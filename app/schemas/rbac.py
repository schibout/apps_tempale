from collections.abc import Iterable
from enum import StrEnum

from app.schemas.admin_permission import Permission, is_self_permission


class RbacAudience(StrEnum):
    """Population a role or permission set is meant for."""

    USER = "user"
    ADMIN = "admin"


def permissions_allowed_for(
    audience: RbacAudience, permissions: Iterable[Permission]
) -> bool:
    """Return whether every permission is admissible for the audience.

    The ``user`` audience only admits self-service (``self.*``) keys; the
    ``admin`` audience admits any permission.
    """
    if audience is RbacAudience.USER:
        return all(is_self_permission(perm) for perm in permissions)
    return True
