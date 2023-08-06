from nonebot import logger
from nonebot.adapters.qqguild import Bot
from nonebot.adapters.qqguild.api import User
from nonebot.exception import ActionFailed


async def get_bot_nickname(bot: Bot, raise_on_failed: bool = False) -> str:
    try:
        user: User = await bot.me()
        return user.username
    except ActionFailed as e:
        if raise_on_failed:
            raise e
        else:
            err_msg = f"获取昵称失败 ActionFailed bot=<{bot.type} {bot.self_id}> exception={e}"
            logger.warning(err_msg)
            return bot.self_id


__all__ = ("get_bot_nickname",)
