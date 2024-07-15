from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.handlers.admin.ban_handler import handle_ban
from bot.handlers.admin.blast_handler import handle_blast
from bot.handlers.admin.catalog_handler import handle_manage_catalog
from bot.handlers.admin.face_swap_handler import handle_manage_face_swap
from bot.handlers.admin.promo_code import handle_create_promo_code
from bot.handlers.admin.statistics_handler import handle_statistics
from bot.keyboards.admin.admin import build_admin_keyboard, build_developer_keyboard
from bot.locales.main import get_user_language, get_localization
from bot.utils.is_admin import is_admin
from bot.utils.is_developer import is_developer

admin_router = Router()


@admin_router.message(Command("admin"))
async def admin(message: Message, state: FSMContext):
    await state.clear()

    if is_admin(str(message.chat.id)):
        user_language_code = await get_user_language(str(message.chat.id), state.storage)

        reply_markup = build_admin_keyboard(user_language_code)
        await message.answer(
            text=get_localization(user_language_code).ADMIN_INFO,
            reply_markup=reply_markup,
        )
    elif is_developer(str(message.chat.id)):
        user_language_code = await get_user_language(str(message.chat.id), state.storage)

        reply_markup = build_developer_keyboard(user_language_code)
        await message.answer(
            text=get_localization(user_language_code).DEVELOPER_INFO,
            reply_markup=reply_markup,
        )


@admin_router.callback_query(lambda c: c.data.startswith('admin:'))
async def handle_admin_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    if action == 'create_promo_code':
        await handle_create_promo_code(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'manage_face_swap':
        await handle_manage_face_swap(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'manage_catalog':
        await handle_manage_catalog(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'statistics':
        await handle_statistics(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'blast':
        await handle_blast(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'ban':
        await handle_ban(callback_query.message, str(callback_query.from_user.id), state)


@admin_router.callback_query(lambda c: c.data.startswith('developer:'))
async def handle_developer_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    if action == 'manage_face_swap':
        await handle_manage_face_swap(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'manage_catalog':
        await handle_manage_catalog(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'statistics':
        await handle_statistics(callback_query.message, str(callback_query.from_user.id), state)
