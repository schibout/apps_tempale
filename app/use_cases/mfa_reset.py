"""Remove a user's MFA enrollment and end their sessions.

Lives in ``use_cases/`` because both the admin service and the last-resort CLI
need the exact same sequence.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.realtime import account_topic, publish_safe
from app.repositories.user_mfa import delete_mfa
from app.repositories.user_session import flag_sessions_revoked, revoke_all_sessions
from app.schemas.account import AccountEvent, AccountEventType


async def reset_user_mfa(session: AsyncSession, user_id: uuid.UUID) -> int:
    """Delete the enrollment, revoke every session and return how many ended.

    Sessions must go too: their tokens carry an ``mfa`` claim proven with the
    authenticator that is being removed.
    """
    await delete_mfa(session, user_id)
    revoked = await revoke_all_sessions(session, user_id=user_id)
    if revoked:
        await flag_sessions_revoked([row.id for row in revoked])
        await publish_safe(
            account_topic(user_id),
            AccountEvent(type=AccountEventType.SESSIONS_REVOKED),
        )
    return len(revoked)
