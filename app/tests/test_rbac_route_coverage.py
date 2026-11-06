"""Every route is either guarded by an RBAC permission or explicitly classified.

A new route that is neither labelled with a permission (``__rbac_permission__``
on its dependency) nor listed below fails this test. Fix the route, not the list,
unless the route is genuinely outside RBAC.
"""

from collections.abc import Iterator

from fastapi.dependencies.models import Dependant
from fastapi.routing import APIRoute, APIWebSocketRoute
from starlette.routing import Route

from app.api.deps import get_current_superadmin
from app.main import app
from app.schemas.admin_permission import Permission

PREFIX = "/api/v1"

Endpoint = tuple[str, str]

# HTTP routes outside RBAC. Everything here either serves the account's own
# identity and session, or carries no user data at all.
SOCLE_ROUTES: frozenset[Endpoint] = frozenset(
    {
        # Authentication flow: runs before (or in order to obtain) a session.
        ("POST", f"{PREFIX}/auth/login"),
        ("POST", f"{PREFIX}/auth/refresh"),
        ("POST", f"{PREFIX}/auth/logout"),
        ("POST", f"{PREFIX}/auth/register"),
        ("POST", f"{PREFIX}/auth/verify-email"),
        ("POST", f"{PREFIX}/auth/forgot-password"),
        ("POST", f"{PREFIX}/auth/reset-password"),
        ("POST", f"{PREFIX}/auth/resend-verification"),
        ("PATCH", f"{PREFIX}/auth/change-password"),
        # MFA (dormant): second-factor handshake, no user data.
        ("POST", f"{PREFIX}/auth/mfa/verify"),
        ("POST", f"{PREFIX}/auth/mfa/recovery"),
        ("POST", f"{PREFIX}/auth/mfa/enroll/start"),
        ("POST", f"{PREFIX}/auth/mfa/enroll/confirm"),
        # The account's own identity, sessions and lifecycle.
        ("GET", f"{PREFIX}/users/me"),
        ("GET", f"{PREFIX}/users/me/sessions"),
        ("DELETE", f"{PREFIX}/users/me/sessions"),
        ("DELETE", f"{PREFIX}/users/me/sessions/{{session_id}}"),
        ("DELETE", f"{PREFIX}/users/me"),
        ("POST", f"{PREFIX}/users/me/reactivate"),
        # Public, user-independent content.
        ("GET", f"{PREFIX}/settings/public"),
        ("GET", f"{PREFIX}/announcements/active"),
        # Operational endpoints without user data.
        ("GET", f"{PREFIX}/health/live"),
        ("GET", f"{PREFIX}/health/ready"),
        ("GET", "/metrics"),
        ("GET", f"{PREFIX}/openapi.json"),
        ("GET", "/docs"),
        ("GET", "/docs/oauth2-redirect"),
        ("GET", "/redoc"),
    }
)

# Admin routes guarded by ``CurrentSuperAdmin`` instead of a permission: these
# actions change who holds the top tier, so no grantable key can unlock them.
SUPERADMIN_ONLY_ROUTES: dict[Endpoint, str] = {
    ("POST", f"{PREFIX}/admin/admins/transfer-root"): "hands the root account over",
    ("POST", f"{PREFIX}/admin/admins/transfer-root/confirm"): "confirms the handover",
    ("POST", f"{PREFIX}/admin/admins/{{user_id}}/promote"): "grants the admin tier",
    ("POST", f"{PREFIX}/admin/admins/{{user_id}}/demote"): "revokes the admin tier",
}

# WebSocket routes have no dependency tree: the permission is checked in the
# handler (and re-checked live by ``permission_watcher``). Behaviour is covered
# by the functional tests of each socket.
WEBSOCKET_PERMISSIONS: dict[str, str | None] = {
    f"{PREFIX}/users/me/events": None,  # socle: the account's own event stream
    f"{PREFIX}/notifications/ws": Permission.SELF_NOTIFICATIONS_READ,
    f"{PREFIX}/support/ws": Permission.SELF_SUPPORT_READ,
    f"{PREFIX}/admin/support/ws": Permission.SUPPORT_READ,
}


def _dependants(dependant: Dependant) -> Iterator[Dependant]:
    for sub in dependant.dependencies:
        yield sub
        yield from _dependants(sub)


def _permissions(route: APIRoute) -> list[Permission]:
    """Return every permission key declared by the route's dependencies."""
    found: list[Permission] = []
    for sub in _dependants(route.dependant):
        label = getattr(sub.call, "__rbac_permission__", None)
        if label is None:
            continue
        found.extend(label if isinstance(label, tuple) else [label])
    return found


def _is_superadmin_only(route: APIRoute) -> bool:
    return any(
        sub.call is get_current_superadmin for sub in _dependants(route.dependant)
    )


def _http_endpoints(route: APIRoute | Route) -> list[Endpoint]:
    methods = sorted((route.methods or set()) - {"HEAD", "OPTIONS"})
    return [(method, route.path) for method in methods]


def test_every_http_route_is_classified() -> None:
    problems: list[str] = []
    seen_socle: set[Endpoint] = set()
    seen_superadmin: set[Endpoint] = set()

    for route in app.routes:
        if isinstance(route, APIWebSocketRoute):
            continue
        if not isinstance(route, (APIRoute, Route)):
            problems.append(f"unknown route type {type(route).__name__}: {route}")
            continue
        permissions = _permissions(route) if isinstance(route, APIRoute) else []
        is_admin = route.path.startswith(f"{PREFIX}/admin/")
        for endpoint in _http_endpoints(route):
            label = f"{endpoint[0]} {endpoint[1]}"
            if is_admin:
                if permissions:
                    continue
                if endpoint in SUPERADMIN_ONLY_ROUTES:
                    seen_superadmin.add(endpoint)
                    if not (isinstance(route, APIRoute) and _is_superadmin_only(route)):
                        problems.append(
                            f"{label}: listed superadmin-only but not guarded"
                        )
                else:
                    problems.append(f"{label}: admin route without a permission")
            elif endpoint in SOCLE_ROUTES:
                seen_socle.add(endpoint)
            elif permissions and all(p.startswith("self.") for p in permissions):
                continue
            else:
                problems.append(f"{label}: neither self.* permission nor socle")

    problems += [f"stale SOCLE_ROUTES entry {e}" for e in SOCLE_ROUTES - seen_socle]
    problems += [
        f"stale SUPERADMIN_ONLY_ROUTES entry {e}"
        for e in set(SUPERADMIN_ONLY_ROUTES) - seen_superadmin
    ]
    assert not problems, "\n".join(sorted(problems))


def test_every_websocket_route_is_classified() -> None:
    paths = {r.path for r in app.routes if isinstance(r, APIWebSocketRoute)}
    assert paths == set(WEBSOCKET_PERMISSIONS)
