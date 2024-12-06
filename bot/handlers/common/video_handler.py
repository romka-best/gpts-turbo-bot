from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.locales.main import get_user_language, get_localization

video_router = Router()


@video_router.message(F.video)
async def video(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    await message.reply(
        text=get_localization(user_language_code).VIDEO_FORBIDDEN_ERROR,
        allow_sending_without_reply=True,
    )
