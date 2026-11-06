"""Compute what an account may do from its roles, sets and direct grants.

Lives in ``use_cases/`` because the API guards, the ``/users/me`` payload and the
admin services all need the same answer. The cache only ever holds what the
database returned: a Redis failure or an unreadable entry falls back to the
database, while a database failure propagates, so no failure can grant anything.
"""

import json
import logging
import uuid
from datetime import UTC, datetime

from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.redis import get_redis
from app.models.user import User
from app.repositories.admin.permission import get_user_permissions
from app.repositories.rbac import (
    get_assigned_permissions,
    get_next_assignment_expiry,
)
from app.schemas.admin_permission import Permission, is_self_permission
from app.schemas.user import SystemRole
from app.utils import utc_now

logger = logging.getLogger(__name__)

_VERSION_KEY = "rbac:version"
# RuntimeError is what ``get_redis`` raises while the client is not initialized.
_REDIS_FAILURES = (RedisError, RuntimeError, OSError)


def _cache_key(version: str | int, user_id: uuid.UUID) -> str:
    """Build the Redis key of an account's permissions for a cache version."""
    return f"perms:{version}:{user_id}"


def _decode_cached(raw: str | None) -> set[Permission] | None:
    """Return the permissions of a cache entry, or None if absent or unreadable."""
    if raw is None:
        return None
    try:
        values = json.loads(raw)
        if not isinstance(values, list):
            return None
        return {Permission(value) for value in values}
    except (ValueError, TypeError):
        return None


async def _read_cache(user_id: uuid.UUID) -> tuple[str | None, set[Permission] | None]:
    """Return the account's cache key and entry, or no key if Redis is unusable.

    The version is read before the database is, so an entry computed while a
    global invalidation happens lands under the old version and is never served.
    """
    try:
        redis = get_redis()
        version = await redis.get(_VERSION_KEY) or 0
        key = _cache_key(version, user_id)
        return key, _decode_cached(await redis.get(key))
    except _REDIS_FAILURES as exc:
        logger.warning("Permission cache read failed: %s", exc)
        return None, None


def _cache_ttl(next_expiry: datetime | None) -> int:
    """Return the entry's lifetime in seconds, capped at the next expiry."""
    if next_expiry is None:
        return settings.RBAC_CACHE_TTL_SECONDS
    # SQLite hands timezone-aware columns back naive; every stored date is UTC.
    if next_expiry.tzinfo is None:
        next_expiry = next_expiry.replace(tzinfo=UTC)
    # Rounded down so the entry can never outlive the assignment it reflects.
    remaining = int((next_expiry - utc_now()).total_seconds())
    return min(settings.RBAC_CACHE_TTL_SECONDS, remaining)


async def _write_cache(
    key: str, permissions: set[Permission], next_expiry: datetime | None
) -> None:
    """Store the account's permissions, unless they are about to change anyway."""
    ttl = _cache_ttl(next_expiry)
    if ttl < 1:
        return
    payload = json.dumps(sorted(permission.value for permission in permissions))
    try:
        await get_redis().set(key, payload, ex=ttl)
    except _REDIS_FAILURES as exc:
        logger.warning("Permission cache write failed: %s", exc)


async def _read_permissions(
    session: AsyncSession, user_id: uuid.UUID, now: datetime
) -> set[Permission]:
    """Return the union of the assignments valid at ``now`` and the direct grants."""
    assigned = await get_assigned_permissions(session, user_id, now)
    return assigned | set(await get_user_permissions(session, user_id))


async def get_effective_permissions_db(
    session: AsyncSession, user_id: uuid.UUID
) -> set[Permission]:
    """Return an account's permissions straight from the database."""
    return await _read_permissions(session, user_id, utc_now())


async def get_effective_permissions(
    session: AsyncSession, user: User
) -> set[Permission]:
    """Return an account's permissions: every key for a superadmin, else cached."""
    if user.role == SystemRole.SUPERADMIN:
        return set(Permission)

    key, cached = await _read_cache(user.id)
    if cached is not None:
        return cached

    now = utc_now()
    permissions = await _read_permissions(session, user.id, now)
    if key is not None:
        next_expiry = await get_next_assignment_expiry(session, user.id, now)
        await _write_cache(key, permissions, next_expiry)
    return permissions


async def invalidate_user_permissions(user_id: uuid.UUID) -> None:
    """Forget one account's cached permissions.

    A Redis failure is logged, not raised: the change it follows is already
    committed, and the stale entry dies with its TTL at the latest.
    """
    try:
        redis = get_redis()
        version = await redis.get(_VERSION_KEY) or 0
        await redis.delete(_cache_key(version, user_id))
    except _REDIS_FAILURES as exc:
        logger.error("Permission cache invalidation failed: %s", exc)


async def invalidate_all_permissions() -> None:
    """Forget every account's cached permissions by moving to a new cache version.

    A Redis failure is logged, not raised, as in ``invalidate_user_permissions``.
    """
    try:
        await get_redis().incr(_VERSION_KEY)
    except _REDIS_FAILURES as exc:
        logger.error("Permission cache invalidation failed: %s", exc)


def _tier_allows(user: User, permission: Permission) -> bool:
    """Return whether the account's tier may use the key: outside it, ``self.*`` only."""
    return user.role in (
        SystemRole.ADMIN,
        SystemRole.SUPERADMIN,
    ) or is_self_permission(permission)


async def user_has_permission(
    session: AsyncSession, user: User, permission: Permission
) -> bool:
    """Return whether ``user`` may exercise ``permission`` (superadmin bypass).

    The tier gate lives here so the answer is safe even if a non-admin reaches
    an admin key: a demoted account whose grant rows linger, or a caller that
    skips ``CurrentAdminUser``.
    """
    if user.role == SystemRole.SUPERADMIN:
        return True
    if not _tier_allows(user, permission):
        return False
    return permission in await get_effective_permissions(session, user)


async def get_usable_permissions(session: AsyncSession, user: User) -> list[Permission]:
    """Return the sorted keys ``user_has_permission`` accepts for this account."""
    effective = await get_effective_permissions(session, user)
    return sorted(key for key in effective if _tier_allows(user, key))
