import uuid
from datetime import datetime

from sqlalchemy import ColumnElement, Select, delete, func, or_, select, union
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac_catalog import (
    DEFAULT_USER_ROLE_ID,
    DEFAULT_USER_ROLE_KEY,
    SYSTEM_PERMISSION_SETS,
    SYSTEM_ROLES,
)
from app.models.rbac import (
    RbacPermissionSet,
    RbacPermissionSetItem,
    RbacRole,
    RbacRolePermissionSet,
    RbacUserPermissionSet,
    RbacUserRole,
)
from app.schemas.admin_permission import Permission
from app.schemas.rbac import RbacAudience

# A losing process only conflicts once per concurrent winner, and the winner's
# committed rows are visible to the retry, so a few attempts are enough.
_CATALOG_SYNC_ATTEMPTS = 3

# Valid keys snapshot so an item left over from a removed enum member is skipped
# rather than raising when materialised back into ``Permission``.
_VALID_PERMISSIONS = {perm.value for perm in Permission}


async def _sync_permission_sets(session: AsyncSession) -> dict[str, uuid.UUID]:
    """Upsert the system sets and their items; return their ``key -> id`` map."""
    keys = [definition.key for definition in SYSTEM_PERMISSION_SETS]
    existing = await session.execute(
        select(RbacPermissionSet).where(RbacPermissionSet.key.in_(keys))
    )
    rows = {row.key: row for row in existing.scalars().all()}

    for definition in SYSTEM_PERMISSION_SETS:
        row = rows.get(definition.key)
        if row is None:
            row = RbacPermissionSet(id=uuid.uuid4(), key=definition.key)
            session.add(row)
            rows[definition.key] = row
        row.name = definition.name
        row.description = definition.description
        row.audience = definition.audience.value
        row.is_system = True
    await session.flush()

    ids = {key: row.id for key, row in rows.items()}
    stored = await session.execute(
        select(RbacPermissionSetItem.set_id, RbacPermissionSetItem.permission).where(
            RbacPermissionSetItem.set_id.in_(list(ids.values()))
        )
    )
    current = {(set_id, permission) for set_id, permission in stored.all()}
    wanted = {
        (ids[definition.key], permission.value)
        for definition in SYSTEM_PERMISSION_SETS
        for permission in definition.permissions
    }
    for set_id, permission in sorted(current - wanted):
        await session.execute(
            delete(RbacPermissionSetItem).where(
                RbacPermissionSetItem.set_id == set_id,
                RbacPermissionSetItem.permission == permission,
            )
        )
    session.add_all(
        RbacPermissionSetItem(set_id=set_id, permission=permission)
        for set_id, permission in sorted(wanted - current)
    )
    await session.flush()
    return ids


async def _sync_roles(session: AsyncSession, set_ids: dict[str, uuid.UUID]) -> None:
    """Upsert the system roles and restore their set memberships."""
    keys = [definition.key for definition in SYSTEM_ROLES]
    existing = await session.execute(select(RbacRole).where(RbacRole.key.in_(keys)))
    rows = {row.key: row for row in existing.scalars().all()}

    for definition in SYSTEM_ROLES:
        row = rows.get(definition.key)
        if row is None:
            role_id = (
                DEFAULT_USER_ROLE_ID
                if definition.key == DEFAULT_USER_ROLE_KEY
                else uuid.uuid4()
            )
            row = RbacRole(id=role_id, key=definition.key)
            session.add(row)
            rows[definition.key] = row
        row.name = definition.name
        row.description = definition.description
        row.audience = definition.audience.value
        row.is_system = True
    await session.flush()

    role_ids = {key: row.id for key, row in rows.items()}
    stored = await session.execute(
        select(RbacRolePermissionSet.role_id, RbacRolePermissionSet.set_id).where(
            RbacRolePermissionSet.role_id.in_(list(role_ids.values()))
        )
    )
    current = {(role_id, set_id) for role_id, set_id in stored.all()}
    wanted = {
        (role_ids[definition.key], set_ids[set_key])
        for definition in SYSTEM_ROLES
        for set_key in definition.set_keys
    }
    for role_id, set_id in sorted(current - wanted):
        await session.execute(
            delete(RbacRolePermissionSet).where(
                RbacRolePermissionSet.role_id == role_id,
                RbacRolePermissionSet.set_id == set_id,
            )
        )
    session.add_all(
        RbacRolePermissionSet(role_id=role_id, set_id=set_id)
        for role_id, set_id in sorted(wanted - current)
    )
    await session.flush()


async def _sync_catalog(session: AsyncSession) -> None:
    """Bring the stored system sets and roles in line with the code."""
    set_ids = await _sync_permission_sets(session)
    await _sync_roles(session, set_ids)


async def ensure_rbac_catalog(session: AsyncSession) -> None:
    """Create the system sets and roles and restore their content from the code.

    Idempotent and safe when several processes boot together: a uniqueness
    conflict means another process inserted the same row first, so the work is
    rolled back and redone against what that process committed.
    """
    for attempt in range(1, _CATALOG_SYNC_ATTEMPTS + 1):
        try:
            await _sync_catalog(session)
            await session.commit()
            return
        except IntegrityError:
            await session.rollback()
            if attempt == _CATALOG_SYNC_ATTEMPTS:
                raise


async def assign_default_role(session: AsyncSession, user_id: uuid.UUID) -> None:
    """Give an account the default role, in the caller's open transaction.

    Flushes without committing so the caller can persist the account and its
    role atomically. Does nothing if the account already holds the role.
    """
    stmt = select(RbacUserRole.id).where(
        RbacUserRole.user_id == user_id,
        RbacUserRole.role_id == DEFAULT_USER_ROLE_ID,
    )
    if (await session.execute(stmt)).first() is not None:
        return
    session.add(RbacUserRole(user_id=user_id, role_id=DEFAULT_USER_ROLE_ID))
    await session.flush()


def _keys_through_roles(
    user_id: uuid.UUID, assignment_filter: ColumnElement[bool]
) -> Select:
    """Select the keys of an account's role assignments passing the filter."""
    return (
        select(RbacPermissionSetItem.permission)
        .join(
            RbacRolePermissionSet,
            RbacRolePermissionSet.set_id == RbacPermissionSetItem.set_id,
        )
        .join(RbacUserRole, RbacUserRole.role_id == RbacRolePermissionSet.role_id)
        .where(RbacUserRole.user_id == user_id, assignment_filter)
    )


def _keys_through_sets(
    user_id: uuid.UUID, assignment_filter: ColumnElement[bool]
) -> Select:
    """Select the keys of an account's direct set assignments passing the filter."""
    return (
        select(RbacPermissionSetItem.permission)
        .join(
            RbacUserPermissionSet,
            RbacUserPermissionSet.set_id == RbacPermissionSetItem.set_id,
        )
        .where(RbacUserPermissionSet.user_id == user_id, assignment_filter)
    )


async def _read_keys(
    session: AsyncSession, through_roles: Select, through_sets: Select
) -> set[Permission]:
    """Return the known keys selected by both assignment queries."""
    rows = await session.execute(union(through_roles, through_sets))
    return {Permission(key) for key in rows.scalars() if key in _VALID_PERMISSIONS}


async def get_assigned_permissions(
    session: AsyncSession, user_id: uuid.UUID, now: datetime
) -> set[Permission]:
    """Return the keys an account holds through roles and sets valid at ``now``."""
    return await _read_keys(
        session,
        _keys_through_roles(
            user_id,
            or_(RbacUserRole.expires_at.is_(None), RbacUserRole.expires_at > now),
        ),
        _keys_through_sets(
            user_id,
            or_(
                RbacUserPermissionSet.expires_at.is_(None),
                RbacUserPermissionSet.expires_at > now,
            ),
        ),
    )


async def get_permanent_assigned_permissions(
    session: AsyncSession, user_id: uuid.UUID
) -> set[Permission]:
    """Return the keys an account holds through assignments without an end date."""
    return await _read_keys(
        session,
        _keys_through_roles(user_id, RbacUserRole.expires_at.is_(None)),
        _keys_through_sets(user_id, RbacUserPermissionSet.expires_at.is_(None)),
    )


async def delete_admin_audience_assignments(
    session: AsyncSession, user_id: uuid.UUID
) -> None:
    """Remove an account's non-``user`` roles and sets, in the caller's transaction.

    Flushes without committing, so a tier change and this removal land together.
    The ``user``-audience assignments stay: an account keeps its self-service keys
    whatever its tier.
    """
    admin_roles = select(RbacRole.id).where(
        RbacRole.audience != RbacAudience.USER.value
    )
    admin_sets = select(RbacPermissionSet.id).where(
        RbacPermissionSet.audience != RbacAudience.USER.value
    )
    await session.execute(
        delete(RbacUserRole).where(
            RbacUserRole.user_id == user_id, RbacUserRole.role_id.in_(admin_roles)
        )
    )
    await session.execute(
        delete(RbacUserPermissionSet).where(
            RbacUserPermissionSet.user_id == user_id,
            RbacUserPermissionSet.set_id.in_(admin_sets),
        )
    )
    await session.flush()


async def get_next_assignment_expiry(
    session: AsyncSession, user_id: uuid.UUID, now: datetime
) -> datetime | None:
    """Return when the account's next role or set assignment expires, if any."""
    role_expiry = select(func.min(RbacUserRole.expires_at)).where(
        RbacUserRole.user_id == user_id, RbacUserRole.expires_at > now
    )
    set_expiry = select(func.min(RbacUserPermissionSet.expires_at)).where(
        RbacUserPermissionSet.user_id == user_id,
        RbacUserPermissionSet.expires_at > now,
    )
    expiries = [
        (await session.execute(role_expiry)).scalar_one_or_none(),
        (await session.execute(set_expiry)).scalar_one_or_none(),
    ]
    return min((expiry for expiry in expiries if expiry is not None), default=None)
