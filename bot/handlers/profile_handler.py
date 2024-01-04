from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from bot.database.main import bucket
from bot.database.models.common import Model
from bot.database.models.user import UserGender
from bot.database.operations.user import get_user, update_user
from bot.handlers.face_swap_handler import handle_face_swap
from bot.keyboards.profile import build_profile_keyboard, build_profile_gender_keyboard
from bot.locales.main import get_localization
from bot.states.profile import Profile

profile_router = Router()


@profile_router.message(Command("profile"))
async def profile(message: Message):
    telegram_user = message.from_user

    user_id = str(telegram_user.id)
    user = await get_user(user_id)

    await update_user(user_id, {
        "first_name": telegram_user.first_name,
        "last_name": telegram_user.last_name or "",
        "username": telegram_user.username,
        "is_premium": telegram_user.is_premium or False,
    })

    text = get_localization(user.language_code).profile(user.subscription_type,
                                                        user.gender,
                                                        user.current_model,
                                                        user.monthly_limits,
                                                        user.additional_usage_quota)
    reply_markup = build_profile_keyboard(user.language_code)

    photo_path = f'users/avatars/{user.id}.jpeg'
    photo = bucket.blob(photo_path)
    if photo.exists():
        photo_data = photo.download_as_string()
        await message.answer_photo(photo=BufferedInputFile(photo_data, filename=photo_path),
                                   caption=text,
                                   reply_markup=reply_markup)
    else:
        await message.answer(text=text,
                             reply_markup=reply_markup)


@profile_router.callback_query(lambda c: c.data.startswith('profile:'))
async def handle_profile_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    action = callback_query.data.split(':')[1]

    if action == 'change_photo':
        photo_path = 'users/avatars/example.png'
        photo = bucket.blob(photo_path)
        photo_data = photo.download_as_string()

        await callback_query.message.answer_photo(
            photo=BufferedInputFile(photo_data, filename=photo_path),
            caption=get_localization(user.language_code).SEND_ME_YOUR_PICTURE
        )

        await state.set_state(Profile.waiting_for_photo)
    elif action == 'change_gender':
        reply_markup = build_profile_gender_keyboard(user.language_code)
        await callback_query.message.answer(text=get_localization(user.language_code).TELL_ME_YOUR_GENDER,
                                            reply_markup=reply_markup)


@profile_router.callback_query(lambda c: c.data.startswith('profile_gender:'))
async def handle_profile_gender_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    gender = callback_query.data.split(':')[1]

    user.gender = gender

    await update_user(user.id, {
        "gender": user.gender,
    })

    text_your_gender = get_localization(user.language_code).YOUR_GENDER
    text_gender_male = get_localization(user.language_code).MALE
    text_gender_female = get_localization(user.language_code).FEMALE
    await callback_query.message.edit_text(
        f"{text_your_gender} {text_gender_male if user.gender == UserGender.MALE else text_gender_female}"
    )

    if user.current_model == Model.FACE_SWAP:
        await handle_face_swap(callback_query.message, state, str(callback_query.from_user.id))
