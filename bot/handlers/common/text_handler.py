import time

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.models.common import Model, Quota
from bot.database.operations.user.getters import get_user
from bot.handlers.ai.chat_gpt_handler import handle_chatgpt
from bot.handlers.ai.dalle_handler import handle_dalle
from bot.handlers.ai.face_swap_handler import handle_face_swap
from bot.handlers.ai.music_gen_handler import handle_music_gen
from bot.utils.is_already_processing import is_already_processing
from bot.utils.is_messages_limit_exceeded import is_messages_limit_exceeded
from bot.utils.is_time_limit_exceeded import is_time_limit_exceeded

text_router = Router()


@text_router.message(F.text)
async def handle_text(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    current_time = time.time()

    if user.current_model == Model.GPT3:
        user_quota = Quota.GPT3
    elif user.current_model == Model.GPT4:
        user_quota = Quota.GPT4
    elif user.current_model == Model.DALLE3:
        user_quota = Quota.DALLE3
    elif user.current_model == Model.FACE_SWAP:
        user_quota = Quota.FACE_SWAP
    elif user.current_model == Model.MUSIC_GEN:
        user_quota = Quota.MUSIC_GEN
    else:
        return
    need_exit = (
        await is_time_limit_exceeded(message, state, user, current_time) or
        await is_messages_limit_exceeded(message, user, user_quota) or
        await is_already_processing(message, state, user, current_time)
    )
    if need_exit:
        return
    await state.update_data(last_request_time=current_time)

    if user.current_model == Model.GPT3 or user.current_model == Model.GPT4:
        await handle_chatgpt(message, state, user, user_quota)
    elif user.current_model == Model.DALLE3:
        await handle_dalle(message, state, user)
    elif user.current_model == Model.FACE_SWAP:
        await handle_face_swap(message.bot, str(message.chat.id), state, user.id, message.text)
    elif user.current_model == Model.MUSIC_GEN:
        await handle_music_gen(message.bot, str(message.chat.id), state, user.id, message.text)
