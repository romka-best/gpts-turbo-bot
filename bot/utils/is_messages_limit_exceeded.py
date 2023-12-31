from aiogram.types import Message

from bot.database.models.common import Quota
from bot.database.models.user import User
from bot.locales.main import get_localization


async def is_messages_limit_exceeded(message: Message, user: User, user_quota: Quota):
    if user.monthly_limits[user_quota] < 1 and user.additional_usage_quota[user_quota] < 1:
        await message.reply(get_localization(user.language_code).REACHED_USAGE_LIMIT)
        return True

    return False
