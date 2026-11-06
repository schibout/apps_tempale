"""Generic realtime fan-out bus (used by support tickets and account events).

A thin in-process registry of WebSocket connections (``ConnectionManager``)
sits behind a Redis pub/sub bridge. Services ``publish()`` an event to a Redis
channel; a per-process listener task receives it and delivers it to the local
WebSockets subscribed to that topic. Going through Redis means an event raised
in one worker reaches clients connected to any worker.

Topics are plain strings:
  * ``ticket:{uuid}``  — the thread of a single ticket (its owner + viewing admin)
  * ``admin``          — the global admin feed (new tickets, status changes)
  * ``user:{uuid}``    — a single user's support feed (across all their tickets)
  * ``account:{uuid}`` — a single user's account feed (e.g. RBAC permission changes)
  * ``notifications:{uuid}`` — a single user's persistent in-app notification feed

The Redis channel is the topic prefixed with ``rt:``.

A socket gated by a permission also watches its owner's account topic, and is
closed when a change there takes the permission away.
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager, suppress

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.core.db import AsyncSessionLocal
from app.core.redis import get_redis
from app.models.user import User
from app.repositories.user import get_user_by_id
from app.schemas.admin_permission import Permission
from app.schemas.support import RealtimeEvent
from app.use_cases.permissions import user_has_permission_uncached

logger = logging.getLogger(__name__)

_CHANNEL_PREFIX = "rt:"
_CHANNEL_PATTERN = f"{_CHANNEL_PREFIX}*"
# Close code of a socket that lost its right to stay open (RFC 6455).
_WS_POLICY_VIOLATION = 1008


class ConnectionManager:
    """In-process map of topic -> set of live WebSocket connections."""

    def __init__(self) -> None:
        """Initialise an empty topic registry guarded by an async lock."""
        self._topics: dict[str, set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, topic: str, websocket: WebSocket) -> None:
        """Register an already-accepted WebSocket under a topic."""
        async with self._lock:
            self._topics.setdefault(topic, set()).add(websocket)

    async def disconnect(self, topic: str, websocket: WebSocket) -> None:
        """Remove a WebSocket from a topic, dropping the topic when empty."""
        async with self._lock:
            connections = self._topics.get(topic)
            if connections is None:
                return
            connections.discard(websocket)
            if not connections:
                self._topics.pop(topic, None)

    async def disconnect_all(self, websocket: WebSocket) -> None:
        """Remove a WebSocket from every topic it joined (on socket close).

        A multiplexed socket may sit on several topics (its feed plus a ticket
        thread), so cleanup must sweep them all.
        """
        async with self._lock:
            for topic in list(self._topics.keys()):
                connections = self._topics[topic]
                connections.discard(websocket)
                if not connections:
                    self._topics.pop(topic, None)

    async def broadcast_local(self, topic: str, data: str) -> None:
        """Send a raw text frame to every local WebSocket on ``topic``.

        Iterates a snapshot so a send-triggered disconnect can't mutate the set
        mid-loop. Failed sockets are pruned rather than aborting the broadcast.
        """
        async with self._lock:
            connections = list(self._topics.get(topic, ()))
        if not connections:
            return

        dead: list[WebSocket] = []
        for websocket in connections:
            try:
                await websocket.send_text(data)
            except Exception:  # noqa: BLE001 - a broken socket must not stop fan-out
                dead.append(websocket)

        for websocket in dead:
            await self.disconnect(topic, websocket)


manager = ConnectionManager()

_listener_task: asyncio.Task[None] | None = None


async def publish(topic: str, event: BaseModel) -> None:
    """Publish an event to all subscribers of ``topic`` across processes."""
    await get_redis().publish(f"{_CHANNEL_PREFIX}{topic}", event.model_dump_json())


async def publish_safe(topic: str, event: BaseModel) -> None:
    """Publish without letting a realtime failure break the caller's request."""
    try:
        await publish(topic, event)
    except Exception:  # noqa: BLE001 - realtime is best-effort, never fatal
        logger.exception("Failed to publish realtime event to topic %s", topic)


ADMIN_TOPIC = "admin"


def user_topic(user_id: uuid.UUID) -> str:
    """Realtime topic carrying changes across all of a single user's tickets."""
    return f"user:{user_id}"


def account_topic(user_id: uuid.UUID) -> str:
    """Realtime topic carrying account-level changes for a single user."""
    return f"account:{user_id}"


def notifications_topic(user_id: uuid.UUID) -> str:
    """Realtime topic carrying a single user's in-app notifications."""
    return f"notifications:{user_id}"


async def publish_feeds(owner_id: uuid.UUID, event: RealtimeEvent) -> None:
    """Fan a ticket-summary event out to both the admin queue and its owner's feed.

    Used wherever a ticket changes so the admin queue and the owner's list both
    refresh live, regardless of which side triggered the change.
    """
    await publish_safe(ADMIN_TOPIC, event)
    await publish_safe(user_topic(owner_id), event)


# --- Permission watch --------------------------------------------------------


class _WakeOnFrame:
    """Topic subscriber that only remembers that a frame arrived."""

    def __init__(self) -> None:
        """Start with no frame pending."""
        self._arrived = asyncio.Event()

    async def send_text(self, _data: str) -> None:
        """Note the frame; its content does not matter, only the re-check does."""
        self._arrived.set()

    async def wait(self) -> None:
        """Wait for a frame, folding those that arrive together into one wake-up."""
        await self._arrived.wait()
        self._arrived.clear()


async def _still_holds(user_id: uuid.UUID, permission: Permission) -> bool:
    """Return whether the account may still use the key, refusing on any failure.

    Uses a short session of its own, since the watch outlives any request, and
    reloads the account because its tier or activation may be what changed.
    """
    try:
        async with AsyncSessionLocal() as session:
            user = await get_user_by_id(session, user_id=user_id)
            if user is None or not user.is_active:
                return False
            return await user_has_permission_uncached(session, user, permission)
    except Exception:  # noqa: BLE001 - an unanswered check must not leave it open
        logger.exception("Socket permission check failed for user %s", user_id)
        return False


async def _watch_permission(
    websocket: WebSocket, user_id: uuid.UUID, permission: Permission
) -> None:
    """Close the socket once a change on the account topic removes the key.

    The first check runs after the subscription, so a change published between
    the caller's own check and this point is not missed.
    """
    topic = account_topic(user_id)
    signal = _WakeOnFrame()
    await manager.connect(topic, signal)
    try:
        while await _still_holds(user_id, permission):
            await signal.wait()
    finally:
        await manager.disconnect(topic, signal)
    await manager.disconnect_all(websocket)
    # The client may have left in the meantime: nothing is left to close then.
    with suppress(RuntimeError, WebSocketDisconnect):
        await websocket.close(code=_WS_POLICY_VIOLATION)


def close_on_permission_loss(
    websocket: WebSocket, user: User, permission: Permission
) -> asyncio.Task[None]:
    """Watch an accepted socket and close it when ``user`` loses ``permission``.

    Works with any key. The caller owns the returned task and cancels it when
    the socket ends. Pass ``requires`` to the ``serve_*`` functions rather than
    calling this directly: they start the watch after the handshake.
    """
    return asyncio.create_task(_watch_permission(websocket, user.id, permission))


# --- Multiplexed WebSocket serving -----------------------------------------

_TICKET_TOPIC_PREFIX = "ticket:"

# An authorize callback decides whether the caller may join a ticket thread.
AuthorizeTicket = Callable[[uuid.UUID], Awaitable[bool]]


def _parse_ticket_topic(topic: str) -> uuid.UUID | None:
    """Return the ticket UUID for a ``ticket:{uuid}`` topic, else ``None``."""
    if not topic.startswith(_TICKET_TOPIC_PREFIX):
        return None
    try:
        return uuid.UUID(topic[len(_TICKET_TOPIC_PREFIX) :])
    except ValueError:
        return None


async def _handle_command(
    websocket: WebSocket, raw: str, authorize_ticket: AuthorizeTicket
) -> None:
    """Apply one client ``subscribe``/``unsubscribe`` frame to a ticket topic.

    Only ``ticket:{uuid}`` topics are client-controllable, and a subscribe is
    gated by ``authorize_ticket``; anything else is ignored.
    """
    try:
        message = json.loads(raw)
    except (ValueError, TypeError):
        return
    if not isinstance(message, dict):
        return
    action = message.get("action")
    topic = message.get("topic")
    if action not in ("subscribe", "unsubscribe") or not isinstance(topic, str):
        return
    ticket_id = _parse_ticket_topic(topic)
    if ticket_id is None:
        return
    if action == "subscribe":
        if await authorize_ticket(ticket_id):
            await manager.connect(topic, websocket)
    else:
        await manager.disconnect(topic, websocket)


@asynccontextmanager
async def _serving(
    websocket: WebSocket, topic: str, requires: tuple[User, Permission] | None
) -> AsyncIterator[None]:
    """Hold a socket open on ``topic``, watching ``requires``, until it closes."""
    await websocket.accept()
    await manager.connect(topic, websocket)
    watcher = close_on_permission_loss(websocket, *requires) if requires else None
    try:
        yield
    except WebSocketDisconnect:
        pass
    finally:
        if watcher is not None:
            watcher.cancel()
            await asyncio.gather(watcher, return_exceptions=True)
        await manager.disconnect_all(websocket)


async def serve_multiplex(
    websocket: WebSocket,
    *,
    feed_topic: str,
    authorize_ticket: AuthorizeTicket,
    requires: tuple[User, Permission] | None = None,
) -> None:
    """Run a multiplexed support socket: one feed topic plus on-demand tickets.

    The socket is auto-subscribed to ``feed_topic`` (the caller's user or admin
    feed). The client may then send ``{"action": "subscribe"|"unsubscribe",
    "topic": "ticket:<uuid>"}`` frames to follow a single ticket thread, gated by
    ``authorize_ticket``. Every joined topic is dropped when the socket closes.
    The socket must already be authenticated; it is accepted here. With
    ``requires`` (the user and the key), it is closed when the user loses the key.
    """
    async with _serving(websocket, feed_topic, requires):
        while True:
            raw = await websocket.receive_text()
            await _handle_command(websocket, raw, authorize_ticket)


async def serve_account_socket(
    websocket: WebSocket,
    *,
    topic: str,
    requires: tuple[User, Permission] | None = None,
) -> None:
    """Run a notification-only socket subscribed to a single ``topic``.

    The client sends nothing; the loop only awaits ``receive_text`` so a close
    is detected and the socket is unsubscribed. The socket must already be
    authenticated; it is accepted here. With ``requires`` (the user and the key),
    it is closed when the user loses the key.
    """
    async with _serving(websocket, topic, requires):
        while True:
            await websocket.receive_text()


async def _listen() -> None:
    """Bridge Redis pub/sub messages to local WebSocket connections."""
    pubsub = get_redis().pubsub()
    await pubsub.psubscribe(_CHANNEL_PATTERN)
    try:
        async for raw in pubsub.listen():
            if raw.get("type") != "pmessage":
                continue
            channel = raw["channel"]
            topic = channel[len(_CHANNEL_PREFIX) :]
            await manager.broadcast_local(topic, raw["data"])
    except asyncio.CancelledError:
        raise
    except Exception:  # noqa: BLE001 - listener must survive transient errors
        logger.exception("Support realtime listener crashed")
    finally:
        await pubsub.punsubscribe(_CHANNEL_PATTERN)
        await pubsub.aclose()


async def start_realtime() -> None:
    """Start the background Redis -> WebSocket listener task."""
    global _listener_task
    if _listener_task is None:
        _listener_task = asyncio.create_task(_listen())


async def stop_realtime() -> None:
    """Cancel the listener task and wait for it to unwind."""
    global _listener_task
    if _listener_task is not None:
        _listener_task.cancel()
        try:
            await _listener_task
        except asyncio.CancelledError:
            pass
        _listener_task = None
