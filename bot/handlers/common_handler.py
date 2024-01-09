from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.main import firebase
from bot.database.operations.user import get_user
from bot.helpers.initialize_user_for_the_first_time import initialize_user_for_the_first_time
from bot.utils.is_admin import is_admin

from bot.locales.main import get_localization

common_router = Router()


@common_router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user(str(message.from_user.id))
    if not user:
        chat_title = get_localization(message.from_user.language_code).DEFAULT_CHAT_TITLE
        transaction = firebase.db.transaction()
        await initialize_user_for_the_first_time(transaction, message.from_user, str(message.chat.id), chat_title)

    greeting = get_localization(user.language_code if user else message.from_user.language_code).START
    await message.answer(greeting)


@common_router.message(Command("help"))
async def help(message: Message):
    user = await get_user(str(message.from_user.id))

    admin_commands = get_localization(user.language_code).COMMANDS_ADMIN
    additional_text = admin_commands if is_admin(str(message.chat.id)) else ""

    await message.answer(text=f"{get_localization(user.language_code).COMMANDS}{additional_text}")


@common_router.callback_query(lambda c: c.data.endswith(':close'))
async def handle_close_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    await callback_query.message.delete()


@common_router.callback_query(lambda c: c.data.endswith(':cancel'))
async def handle_cancel_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await callback_query.message.delete()

    await state.clear()
