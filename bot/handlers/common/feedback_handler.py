from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.config import config
from bot.database.operations.feedback.writers import write_feedback
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.keyboards.admin.feedback import build_manage_feedback_keyboard

from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.feedback import Feedback

feedback_router = Router()


@feedback_router.message(Command("feedback"))
async def handle_feedback(message: Message, state: FSMContext):
    await state.clear()

    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    reply_markup = build_cancel_keyboard(user_language_code)
    await message.answer(
        text=get_localization(user_language_code).FEEDBACK,
        reply_markup=reply_markup,
    )

    await state.set_state(Feedback.waiting_for_feedback)


@feedback_router.message(Feedback.waiting_for_feedback, F.text, ~F.text.startswith('/'))
async def handle_feedback_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    feedback = await write_feedback(user_id, message.text)

    text = (f"#feedback\n\n"
            f"🚀 <b>Новая обратная связь от пользователя</b>: {user_id} 🚀\n\n"
            f"<code>{message.text}</code>")
    await send_message_to_admins(
        bot=message.bot,
        message=text,
    )

    reply_markup = build_manage_feedback_keyboard(user_language_code, user_id)
    await message.bot.send_message(
        chat_id=config.MODERATOR_ID,
        text=f"<b>{feedback.id} от {user_id}</b>",
        reply_markup=reply_markup,
    )

    await message.reply(text=get_localization(user_language_code).FEEDBACK_SUCCESS)

    await state.clear()


@feedback_router.callback_query(lambda c: c.data.startswith('manage_feedback:'))
async def handle_manage_feedback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    user_id = callback_query.data.split(':')[2]
    user_language_code = await get_user_language(user_id, state.storage)

    if action == "approve":
        user = await get_user(user_id)

        user.balance += 50.00
        await update_user(user_id, {
            "balance": user.balance,
        })

        await callback_query.bot.send_message(
            user_id,
            get_localization(user_language_code).FEEDBACK_APPROVED,
        )
    elif action == "deny":
        await callback_query.bot.send_message(
            user_id,
            get_localization(user_language_code).FEEDBACK_DENIED,
        )

    new_text = f"<b>{callback_query.message.text}</b>\n\n<b>Статус:</b> {'Одобрена ✅' if action == 'approve' else 'Отклонена ❌'}"
    await callback_query.message.edit_text(
        text=new_text,
        reply_markup=None,
    )
