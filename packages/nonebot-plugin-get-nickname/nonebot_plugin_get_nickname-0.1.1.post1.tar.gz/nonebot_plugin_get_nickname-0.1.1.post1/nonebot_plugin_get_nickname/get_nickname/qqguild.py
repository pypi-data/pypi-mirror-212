from typing import Union

from nonebot import logger
from nonebot.adapters.qqguild import Bot
from nonebot.exception import ActionFailed
from nonebot.internal.adapter import Event
from nonebot_plugin_session import Session, SessionIdType, extract_session


async def get_nickname(session_or_event: Union[Session, Event], bot: Bot, *, raise_on_failed: bool = False) -> str:
    if isinstance(session_or_event, Event):
        session = extract_session(bot, session_or_event)
    else:
        session = session_or_event

    try:
        member = await bot.get_member(guild_id=session.id3, user_id=session.id1)
        return member.nick or session.id1
    except ActionFailed as e:
        if raise_on_failed:
            raise e
        else:
            err_msg = f"获取昵称失败 ActionFailed session={session} bot=<{bot.type} {bot.self_id}> exception={e}"
            logger.warning(err_msg)
            return session.get_id(SessionIdType.USER, include_bot_type=False, include_bot_id=False)


__all__ = ("get_nickname",)
