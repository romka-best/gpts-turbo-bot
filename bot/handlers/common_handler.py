from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.main import firebase
from bot.database.operations.user import get_user, update_user
from bot.helpers.initialize_user_for_the_first_time import initialize_user_for_the_first_time
from bot.helpers.update_daily_limits import update_user_monthly_limits
from bot.keyboards.common import build_recommendations_keyboard
from bot.utils.is_admin import is_admin

from bot.locales.main import get_localization

common_router = Router()


@common_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user(str(message.from_user.id))
    if not user:
        chat_title = get_localization(message.from_user.language_code).DEFAULT_CHAT_TITLE
        transaction = firebase.db.transaction()
        await initialize_user_for_the_first_time(transaction, message.from_user, str(message.chat.id), chat_title)
        user = await get_user(str(message.from_user.id))
    elif user and user.is_blocked:
        user.is_blocked = False
        await update_user(user.id, {
            "is_blocked": user.is_blocked,
        })

        batch = firebase.db.batch()
        await update_user_monthly_limits(message.bot, user, batch)
        await batch.commit()

    greeting = get_localization(user.language_code).START
    reply_markup = await build_recommendations_keyboard(user)
    await message.answer(
        text=greeting,
        reply_markup=reply_markup,
    )


@common_router.message(Command("help"))
async def help(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user(str(message.from_user.id))

    admin_commands = get_localization(user.language_code).COMMANDS_ADMIN
    additional_text = admin_commands if is_admin(str(message.chat.id)) else ""

    text = get_localization(user.language_code).COMMANDS
    reply_markup = await build_recommendations_keyboard(user)
    await message.answer(
        text=f"{text}{additional_text}",
        reply_markup=reply_markup,
    )


@common_router.message(Command("info"))
async def info(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user(str(message.from_user.id))

    text = get_localization(user.language_code).INFO
    reply_markup = await build_recommendations_keyboard(user)
    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


@common_router.callback_query(lambda c: c.data.endswith(':close'))
async def handle_close_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    await callback_query.message.delete()


@common_router.callback_query(lambda c: c.data.endswith(':cancel'))
async def handle_cancel_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await callback_query.message.delete()

    await state.clear()
