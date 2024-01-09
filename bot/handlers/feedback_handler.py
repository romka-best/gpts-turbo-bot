from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.operations.feedback import write_feedback
from bot.database.operations.user import get_user
from bot.helpers.send_message_to_admins import send_message_to_admins
from bot.keyboards.feedback import build_feedback_keyboard
from bot.locales.main import get_localization
from bot.states.feedback import Feedback

feedback_router = Router()


@feedback_router.message(Command("feedback"))
async def feedback(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    reply_markup = build_feedback_keyboard(user.language_code)

    await message.answer(text=get_localization(user.language_code).FEEDBACK,
                         reply_markup=reply_markup)

    await state.set_state(Feedback.waiting_for_feedback)


@feedback_router.message(Feedback.waiting_for_feedback)
async def feedback_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    await write_feedback(user.id, message.text)

    text = (f"#feedback\n\n"
            f"🚀 <b>Новая обратная связь от пользователя</b>: {user.id} 🚀\n\n"
            f"<code>{message.text}</code>")
    await send_message_to_admins(message.bot, text)

    await message.reply(text=get_localization(user.language_code).FEEDBACK_SUCCESS)

    await state.clear()


@feedback_router.callback_query(Feedback.waiting_for_feedback, lambda c: c.data == 'cancel')
async def handle_exit_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await callback_query.message.delete()

    await state.clear()
