from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import config, MessageSticker
from bot.database.models.common import Quota
from bot.database.models.user import User
from bot.keyboards.common.common import build_limit_exceeded_keyboard
from bot.locales.main import get_localization, get_user_language


async def is_messages_limit_exceeded(message: Message, state: FSMContext, user: User, user_quota: Quota):
    if user.daily_limits[user_quota] < 1 and user.additional_usage_quota[user_quota] < 1:
        user_language_code = await get_user_language(user.id, state.storage)

        await message.answer_sticker(
            sticker=config.MESSAGE_STICKERS.get(MessageSticker.SAD),
        )

        text = get_localization(user_language_code).REACHED_USAGE_LIMIT
        reply_markup = build_limit_exceeded_keyboard(user_language_code)
        await message.reply(
            text=text,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )

        return True

    return False
