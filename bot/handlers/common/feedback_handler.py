from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.operations.feedback.getters import get_feedbacks_by_user_id
from bot.database.operations.feedback.writers import write_feedback
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins

from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.feedback import Feedback

feedback_router = Router()


@feedback_router.message(Command("feedback"))
async def feedback(message: Message, state: FSMContext):
    await state.clear()

    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    reply_markup = build_cancel_keyboard(user_language_code)
    await message.answer(
        text=get_localization(user_language_code).FEEDBACK,
        reply_markup=reply_markup,
    )

    await state.set_state(Feedback.waiting_for_feedback)


@feedback_router.message(Feedback.waiting_for_feedback, ~F.text.startswith('/'))
async def feedback_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    users_feedbacks = await get_feedbacks_by_user_id(user_id)
    if len(users_feedbacks) == 0:
        user = await get_user(user_id)
        user.balance += 50.00

        await update_user(user_id, {
            "balance": user.balance,
        })

    await write_feedback(user_id, message.text)

    text = (f"#feedback\n\n"
            f"🚀 <b>Новая обратная связь от пользователя</b>: {user_id} 🚀\n\n"
            f"<code>{message.text}</code>")
    await send_message_to_admins(message.bot, text)

    await message.reply(text=get_localization(user_language_code).FEEDBACK_SUCCESS)

    await state.clear()
