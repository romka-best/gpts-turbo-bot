from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.config import config
from bot.database.models.feedback import FeedbackStatus
from bot.database.operations.feedback.getters import get_count_of_approved_feedbacks_by_user_id
from bot.database.operations.feedback.updaters import update_feedback
from bot.database.operations.feedback.writers import write_feedback
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers
from bot.keyboards.admin.feedback import build_manage_feedback_keyboard

from bot.keyboards.common.feedback import build_feedback_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.common.feedback import Feedback

feedback_router = Router()


@feedback_router.message(Command('feedback'))
async def feedback(message: Message, state: FSMContext):
    await state.clear()

    await handle_feedback(message, str(message.from_user.id), state)


async def handle_feedback(message: Message, user_id: str, state: FSMContext):
    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_feedback_keyboard(user_language_code)
    await message.answer(
        text=get_localization(user_language_code).FEEDBACK_INFO,
        reply_markup=reply_markup,
    )

    await state.set_state(Feedback.waiting_for_feedback)


@feedback_router.message(Feedback.waiting_for_feedback, F.text, ~F.text.startswith('/'))
async def handle_feedback_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    feedback = await write_feedback(user_id, message.text)

    text = (f'#feedback\n\n'
            f'🚀 <b>Новая обратная связь от пользователя</b>: {user_id} 🚀\n\n'
            f'<code>{message.text}</code>')
    await send_message_to_admins_and_developers(
        bot=message.bot,
        message=text,
    )

    reply_markup = build_manage_feedback_keyboard(user_language_code, user_id, feedback.id)
    await message.bot.send_message(
        chat_id=config.SUPER_ADMIN_ID,
        text=f'<b>{feedback.id} from {user_id}</b>',
        reply_markup=reply_markup,
    )

    await message.reply(
        text=get_localization(user_language_code).FEEDBACK_SUCCESS,
        allow_sending_without_reply=True,
    )

    await state.clear()


@feedback_router.callback_query(lambda c: c.data.startswith('mf:'))
async def handle_manage_feedback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    user_id = callback_query.data.split(':')[2]
    feedback_id = callback_query.data.split(':')[3]
    user_language_code = await get_user_language(user_id, state.storage)

    status = FeedbackStatus.WAITING
    if action == 'approve':
        user = await get_user(user_id)
        count_of_feedbacks = await get_count_of_approved_feedbacks_by_user_id(user_id)
        if count_of_feedbacks > 2:
            await callback_query.bot.send_message(
                chat_id=user_id,
                text=get_localization(user_language_code).FEEDBACK_APPROVED_WITH_LIMIT_ERROR,
                disable_notification=True,
            )
        else:
            user.balance += 25.00
            await update_user(user_id, {
                'balance': user.balance,
            })

            await callback_query.bot.send_message(
                chat_id=user_id,
                text=get_localization(user_language_code).FEEDBACK_APPROVED,
                disable_notification=True,
            )
        status = FeedbackStatus.APPROVED
    elif action == 'deny':
        await callback_query.bot.send_message(
            chat_id=user_id,
            text=get_localization(user_language_code).FEEDBACK_DENIED,
            disable_notification=True,
        )
        status = FeedbackStatus.DENIED

    await update_feedback(feedback_id, {
        'status': status,
    })

    new_text = f'<b>{callback_query.message.text}</b>\n\n<b>Status:</b> {"Approved ✅" if action == "approve" else "Denied ❌"}'
    await callback_query.message.edit_text(
        text=new_text,
        reply_markup=None,
    )
