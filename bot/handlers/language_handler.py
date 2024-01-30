from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.operations.user import get_user, update_user
from bot.keyboards.common import build_recommendations_keyboard
from bot.keyboards.language import build_language_keyboard
from bot.locales.main import get_localization

language_router = Router()


@language_router.message(Command("language"))
async def language(message: Message, state: FSMContext):
    await state.clear()

    language_code = (await get_user(str(message.from_user.id))).language_code

    reply_markup = build_language_keyboard(language_code)

    await message.answer(text=get_localization(language_code).LANGUAGE,
                         reply_markup=reply_markup)


@language_router.callback_query(lambda c: c.data.startswith('language:'))
async def handle_language_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))
    chosen_language = callback_query.data.split(':')[1]

    user.language_code = chosen_language
    await update_user(user.id, {
        "language_code": user.language_code
    })

    reply_markup = await build_recommendations_keyboard(user)
    await callback_query.message.answer(
        text=get_localization(chosen_language).CHOOSE_LANGUAGE,
        reply_markup=reply_markup,
    )

    await callback_query.message.delete()
