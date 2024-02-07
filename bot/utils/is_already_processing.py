from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import config
from bot.database.models.user import User
from bot.locales.main import get_localization


async def is_already_processing(message: Message, state: FSMContext, user: User, current_time: float):
    user_data = await state.get_data()
    is_processing = user_data.get('is_processing')

    if not is_processing:
        return False

    last_request_time = user_data.get('last_request_time', None)
    time_elapsed = current_time - last_request_time
    if time_elapsed >= config.LIMIT_PROCESSING_SECONDS:
        await state.update_data(is_processing=False)
        return False

    await message.reply(text=get_localization(user.language_code).ALREADY_MAKE_REQUEST)
    return True
