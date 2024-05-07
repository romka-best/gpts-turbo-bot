from datetime import timedelta

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile

from bot.database.main import firebase
from bot.database.models.common import Model
from bot.database.models.user import UserGender, UserSettings
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.ai.face_swap_handler import handle_face_swap
from bot.keyboards.common.common import build_cancel_keyboard
from bot.keyboards.common.profile import build_profile_keyboard, build_profile_gender_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.profile import Profile

profile_router = Router()


@profile_router.message(Command("profile"))
async def profile(message: Message, state: FSMContext):
    await state.clear()

    telegram_user = message.from_user

    user_id = str(telegram_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if (
        user.first_name != telegram_user.first_name or
        user.last_name != telegram_user.last_name or
        user.username != telegram_user.username or
        user.is_premium != telegram_user.is_premium or
        user.language_code != telegram_user.language_code
    ):
        await update_user(user_id, {
            "first_name": telegram_user.first_name,
            "last_name": telegram_user.last_name or "",
            "username": telegram_user.username,
            "is_premium": telegram_user.is_premium or False,
            "language_code": telegram_user.language_code,
        })

    renewal_date = (user.last_subscription_limit_update + timedelta(days=30))
    text = get_localization(user_language_code).profile(
        user.subscription_type,
        user.gender,
        user.current_model,
        user.settings[Model.CHAT_GPT][UserSettings.VERSION],
        user.monthly_limits,
        user.additional_usage_quota,
        renewal_date.strftime("%d.%m.%Y"),
        user.discount,
        user.balance,
    )

    photo_path = f'users/avatars/{user_id}.jpeg'
    try:
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        reply_markup = build_profile_keyboard(user_language_code, True, user.gender != UserGender.UNSPECIFIED)
        await message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=text,
            reply_markup=reply_markup,
        )
    except aiohttp.ClientResponseError:
        reply_markup = build_profile_keyboard(user_language_code, False, user.gender != UserGender.UNSPECIFIED)
        await message.answer(
            text=text,
            reply_markup=reply_markup,
        )


@profile_router.callback_query(lambda c: c.data.startswith('profile:'))
async def handle_profile_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'change_photo':
        photo_path = 'users/avatars/example.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        reply_markup = build_cancel_keyboard(user_language_code)
        await callback_query.message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=get_localization(user_language_code).SEND_ME_YOUR_PICTURE,
            reply_markup=reply_markup
        )

        await state.set_state(Profile.waiting_for_photo)
    elif action == 'change_gender':
        reply_markup = build_profile_gender_keyboard(user_language_code)
        await callback_query.message.answer(
            text=get_localization(user_language_code).TELL_ME_YOUR_GENDER,
            reply_markup=reply_markup,
        )


@profile_router.callback_query(lambda c: c.data.startswith('profile_gender:'))
async def handle_profile_gender_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    gender = callback_query.data.split(':')[1]

    if user.gender != gender:
        user.gender = gender
        await update_user(user.id, {
            "gender": user.gender,
        })

    text_your_gender = get_localization(user_language_code).YOUR_GENDER
    text_gender_male = get_localization(user_language_code).MALE
    text_gender_female = get_localization(user_language_code).FEMALE
    await callback_query.message.edit_text(
        f"{text_your_gender} {text_gender_male if user.gender == UserGender.MALE else text_gender_female}"
    )

    if user.current_model == Model.FACE_SWAP:
        await handle_face_swap(
            callback_query.bot,
            str(callback_query.message.chat.id),
            state,
            str(callback_query.from_user.id),
        )
