import time

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.models.common import Model, Quota
from bot.database.operations.user import get_user
from bot.handlers.chat_gpt_handler import handle_chatgpt
from bot.handlers.dalle_handler import handle_dalle
from bot.handlers.face_swap_handler import handle_face_swap
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
    else:
        return
    need_exit = (await is_time_limit_exceeded(message, state, user, current_time) or
                 await is_messages_limit_exceeded(message, user, user_quota))
    if need_exit:
        return
    await state.update_data(last_request_time=current_time)

    if user_quota == Quota.GPT3 or user_quota == Quota.GPT4:
        await handle_chatgpt(message, state, user, user_quota)
    elif user_quota == Quota.DALLE3:
        await handle_dalle(message, state, user, user_quota)
    elif user_quota == Quota.FACE_SWAP:
        await handle_face_swap(message.bot, str(message.chat.id), state, str(message.from_user.id), message.text)
