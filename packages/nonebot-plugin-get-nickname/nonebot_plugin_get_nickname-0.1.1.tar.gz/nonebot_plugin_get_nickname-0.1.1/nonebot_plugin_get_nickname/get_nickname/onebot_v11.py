from typing import Union

from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot
from nonebot.exception import ActionFailed
from nonebot.internal.adapter import Event
from nonebot_plugin_session import Session, SessionIdType, extract_session, SessionLevel


async def get_nickname(session_or_event: Union[Session, Event], bot: Bot, *, raise_on_failed: bool = False) -> str:
    if isinstance(session_or_event, Event):
        session = extract_session(bot, session_or_event)
    else:
        session = session_or_event

    try:
        if session.level == SessionLevel.LEVEL2:
            user_info = await bot.get_group_member_info(group_id=int(session.id2), user_id=int(session.id1))
            return user_info["card"] or user_info["nickname"]
        else:
            user_info = await bot.get_stranger_info(user_id=int(session.id1))
            return user_info["nickname"]
    except ActionFailed as e:
        if raise_on_failed:
            raise e
        else:
            err_msg = f"获取昵称失败 ActionFailed session={session} bot=<{bot.type} {bot.self_id}> exception={e}"
            logger.warning(err_msg)
            return session.get_id(SessionIdType.USER, include_bot_type=False, include_bot_id=False)


__all__ = ("get_nickname",)
