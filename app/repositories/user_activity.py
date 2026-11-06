import uuid
from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import actor_reference
from app.models.user_activity import UserActivity
from app.schemas.common import ActivityDetails
from app.schemas.user_activity import ResourceType, UserActivityCreate

# Keys of ``UserActivity.details`` that identify a person and must not outlive
# the account they belong to.
ACTIVITY_PII_KEYS = {"email", "first_name", "last_name", "new_email", "ip_address"}

# Rows rewritten per round trip when anonymizing a (possibly large) trail.
_ANONYMIZE_BATCH_SIZE = 500


def _strip_pii(details: ActivityDetails | None) -> ActivityDetails:
    """Return a copy of ``details`` without the personally identifying keys."""
    return {k: v for k, v in (details or {}).items() if k not in ACTIVITY_PII_KEYS}


async def create_user_activity(
    session: AsyncSession, activity_data: UserActivityCreate
) -> UserActivity:
    """Create a new user activity log in the database."""
    db_activity = UserActivity(
        user_id=activity_data.user_id,
        actor_ref=activity_data.actor_ref,
        activity_type=activity_data.activity_type.value,
        resource_type=activity_data.resource_type.value,
        resource_id=activity_data.resource_id,
        details=activity_data.details,
        status=activity_data.status.value,
        status_code=activity_data.status_code,
        ip_address=activity_data.ip_address,
        user_agent=activity_data.user_agent,
    )
    session.add(db_activity)
    await session.commit()
    await session.refresh(db_activity)
    return db_activity


async def anonymize_user_activities(
    session: AsyncSession, user_ids: Sequence[uuid.UUID], deleted_at: datetime
) -> None:
    """Strip PII from the audit trail of accounts about to be deleted.

    Rows owned by the accounts get an ``actor_ref``, a ``user_deleted_at``
    stamp and lose IP, user-agent and PII detail keys. Rows written by other
    actors about those accounts (``resource_type=USER``) only lose PII detail
    keys. Flushes but never commits: the caller deletes the users in the same
    transaction. The ``user_id`` itself is nulled by the FK ``ON DELETE SET NULL``.
    """
    if not user_ids:
        return
    ids = list(user_ids)

    last_id: uuid.UUID | None = None
    while True:
        stmt = select(UserActivity).where(UserActivity.user_id.in_(ids))
        if last_id is not None:
            stmt = stmt.where(UserActivity.id > last_id)
        rows = (
            (
                await session.execute(
                    stmt.order_by(UserActivity.id).limit(_ANONYMIZE_BATCH_SIZE)
                )
            )
            .scalars()
            .all()
        )
        if not rows:
            break
        for row in rows:
            row.actor_ref = actor_reference(str(row.user_id))
            row.user_deleted_at = deleted_at
            row.ip_address = None
            row.user_agent = None
            row.details = _strip_pii(row.details)
        await session.flush()
        last_id = rows[-1].id

    last_id = None
    while True:
        stmt = select(UserActivity).where(
            UserActivity.resource_type == ResourceType.USER.value,
            UserActivity.resource_id.in_(ids),
        )
        if last_id is not None:
            stmt = stmt.where(UserActivity.id > last_id)
        rows = (
            (
                await session.execute(
                    stmt.order_by(UserActivity.id).limit(_ANONYMIZE_BATCH_SIZE)
                )
            )
            .scalars()
            .all()
        )
        if not rows:
            break
        for row in rows:
            row.details = _strip_pii(row.details)
        await session.flush()
        last_id = rows[-1].id


async def purge_anonymized_activities(
    session: AsyncSession, cutoff: datetime, batch_size: int
) -> int:
    """Delete orphaned audit rows older than ``cutoff``, in batches.

    A row is eligible when it has no account (``user_id IS NULL``) and
    ``COALESCE(user_deleted_at, created_at)`` is before ``cutoff``. Commits
    after each batch and returns the number of rows removed.
    """
    total = 0
    while True:
        ids = (
            (
                await session.execute(
                    select(UserActivity.id)
                    .where(
                        UserActivity.user_id.is_(None),
                        func.coalesce(
                            UserActivity.user_deleted_at, UserActivity.created_at
                        )
                        < cutoff,
                    )
                    .limit(batch_size)
                )
            )
            .scalars()
            .all()
        )
        if not ids:
            break
        await session.execute(delete(UserActivity).where(UserActivity.id.in_(ids)))
        await session.commit()
        total += len(ids)
        if len(ids) < batch_size:
            break
    return total
