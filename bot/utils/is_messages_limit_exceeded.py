from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.models.common import Quota
from bot.database.models.user import User
from bot.locales.main import get_localization, get_user_language


async def is_messages_limit_exceeded(message: Message, state: FSMContext, user: User, user_quota: Quota):
    if user.monthly_limits[user_quota] < 1 and user.additional_usage_quota[user_quota] < 1:
        user_language_code = await get_user_language(user.id, state.storage)
        await message.reply(get_localization(user_language_code).REACHED_USAGE_LIMIT)
        return True

    return False
