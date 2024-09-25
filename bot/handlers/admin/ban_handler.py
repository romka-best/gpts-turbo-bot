from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.keyboards.admin.admin import build_admin_keyboard
from bot.keyboards.admin.ban import build_ban_keyboard
from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_user_language, get_localization
from bot.states.ban import Ban

ban_router = Router()


async def handle_ban(message: Message, user_id: str, state: FSMContext):
    await state.clear()

    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_ban_keyboard(user_language_code)
    await message.edit_text(
        text=get_localization(user_language_code).BAN_INFO,
        reply_markup=reply_markup,
    )

    await state.set_state(Ban.waiting_for_user_id)


@ban_router.callback_query(lambda c: c.data.startswith('ban:'))
async def handle_blast_language_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'back':
        reply_markup = build_admin_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_INFO,
            reply_markup=reply_markup,
        )

        await state.clear()
        return


@ban_router.message(Ban.waiting_for_user_id, F.text, ~F.text.startswith('/'))
async def ban_user_id_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    try:
        user_id = int(message.text)
        user = await get_user(str(user_id))

        user.is_banned = not user.is_banned
        await update_user(user.id, {
            'is_banned': user.is_banned,
        })

        if user.is_banned:
            await message.reply(text=get_localization(user_language_code).BAN_SUCCESS)
        else:
            await message.reply(text=get_localization(user_language_code).UNBAN_SUCCESS)

        await state.clear()
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).VALUE_ERROR,
            reply_markup=reply_markup,
        )
