import random
import io
from PIL import Image

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from telegram import constants

from bot.database.main import bucket
from bot.database.models.common import Quota, Currency
from bot.database.models.face_swap_package import FaceSwapPackageName
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserGender
from bot.database.operations.face_swap_package import get_face_swap_package_by_user_id_and_name, \
    write_face_swap_package, update_face_swap_package
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user, update_user
from bot.helpers.send_images import send_images
from bot.integrations.replicateAI import get_face_swap_image
from bot.keyboards.face_swap import build_face_swap_choose_keyboard, build_face_swap_package_keyboard
from bot.keyboards.profile import build_profile_gender_keyboard
from bot.locales.main import get_localization
from bot.states.face_swap import FaceSwap
from bot.states.profile import Profile

face_swap_router = Router()


async def handle_face_swap(message: Message, state: FSMContext, user_id: str):
    user = await get_user(str(user_id))

    if user.gender == UserGender.UNSPECIFIED:
        reply_markup = build_profile_gender_keyboard(user.language_code)
        await message.reply_text(text=get_localization(user.language_code).TELL_ME_YOUR_GENDER,
                                 reply_markup=reply_markup)
    else:
        photo = bucket.blob(f'users/{user.id}.jpeg')
        if photo.exists():
            reply_markup = build_face_swap_choose_keyboard(user.language_code)
            await message.reply_text(text=get_localization(user.language_code).CHOOSE_YOUR_PACKAGE,
                                     reply_markup=reply_markup)
        else:
            await message.reply_text(text=get_localization(user.language_code).SEND_ME_YOUR_PICTURE)
            await state.set_state(Profile.waiting_for_photo)


@face_swap_router.message()
async def face_swap(message: Message, state: FSMContext):
    await handle_face_swap(message, state, user_id=str(message.from_user.id))


@face_swap_router.callback_query(lambda c: c.data.startswith('face_swap_choose:'))
async def handle_face_swap_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    package_name = callback_query.data.split(':')[1]

    face_swap_package = await get_face_swap_package_by_user_id_and_name(user.id, package_name)
    if face_swap_package is None:
        face_swap_package = await write_face_swap_package(user.id, package_name, {
            UserGender.MALE: [],
            UserGender.FEMALE: []
        })
    face_swap_package_quantity = len(getattr(FaceSwapPackageName, package_name)[f"{user.gender}_files"])
    face_swap_package_name = face_swap_package.name
    if face_swap_package.name == FaceSwapPackageName.CELEBRITIES['name']:
        face_swap_package_name = get_localization(user.language_code).CELEBRITIES
    elif face_swap_package_name == FaceSwapPackageName.MOVIE_CHARACTERS['name']:
        face_swap_package_name = get_localization(user.language_code).MOVIE_CHARACTERS
    elif face_swap_package_name == FaceSwapPackageName.PROFESSIONS['name']:
        face_swap_package_name = get_localization(user.language_code).PROFESSIONS
    elif face_swap_package_name == FaceSwapPackageName.SEVEN_WONDERS_OF_THE_ANCIENT_WORLD['name']:
        face_swap_package_name = get_localization(user.language_code).SEVEN_WONDERS_OF_THE_ANCIENT_WORLD

    reply_markup = build_face_swap_package_keyboard(user.language_code)

    await callback_query.message.edit_text(
        text=get_localization(user.language_code).choose_face_swap_package(
            face_swap_package_name,
            user.monthly_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP],
            face_swap_package_quantity,
            len(face_swap_package.used_images[user.gender])),
        reply_markup=reply_markup)

    await state.set_state(FaceSwap.waiting_for_face_swap_quantity)
    await state.update_data(face_swap_package_name=face_swap_package.name)


@face_swap_router.callback_query(lambda c: c.data.startswith('face_swap_package:'))
async def handle_face_swap_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    package_name = callback_query.data.split(':')[1]

    if package_name == 'cancel':
        await callback_query.delete_message()
    elif package_name == 'back':
        user = await get_user(str(callback_query.from_user.id))

        reply_markup = build_face_swap_choose_keyboard(user.language_code)
        await callback_query.message.edit_text(text=get_localization(user.language_code).CHOOSE_YOUR_PACKAGE,
                                               reply_markup=reply_markup)

    await state.clear()


@face_swap_router.message(FaceSwap.waiting_for_face_swap_quantity)
async def face_swap_quantity_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))
    user_data = await state.get_data()

    try:
        quota = user.monthly_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP]
        quantity = int(message.text)
        name = user_data['face_swap_package_name']
        face_swap_package_quantity = len(getattr(FaceSwapPackageName, name)[f"{user.gender}_files"])

        if quota < quantity:
            await message.answer(text=get_localization(user.language_code).face_swap_package_forbidden(quota))
        elif quantity < 1:
            await message.answer(text=get_localization(user.language_code).FACE_SWAP_MIN_ERROR)
        elif face_swap_package_quantity < quantity:
            await message.answer(text=get_localization(user.language_code).FACE_SWAP_MAX_ERROR)
        else:
            await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.UPLOAD_PHOTO)

            user_photo = bucket.blob(f'users/{user.id}.jpeg')
            user_photo.make_public()
            user_photo_link = user_photo.public_url
            face_swap_package = await get_face_swap_package_by_user_id_and_name(user.id, name)
            files = getattr(FaceSwapPackageName, name)[f"{user.gender}_files"]
            images = []
            for _ in range(quantity):
                random_image_name = random.choice(files)
                while random_image_name in face_swap_package.used_images[user.gender]:
                    random_image_name = random.choice(files)
                face_swap_package.used_images[user.gender].append(random_image_name)

                random_image = bucket.blob(
                    f'face_swap/{user.gender.lower()}/{face_swap_package.name.lower()}/{random_image_name}')
                random_image.make_public()
                image_link = random_image.public_url
                image_data = random_image.download_as_bytes()
                image = Image.open(io.BytesIO(image_data))

                width, height = image.size

                face_swap_response = await get_face_swap_image(width, height, image_link, user_photo_link)
                images.append(face_swap_response['image'])

                await write_transaction(user_id=user.id,
                                        type=TransactionType.EXPENSE,
                                        service=ServiceType.FACE_SWAP,
                                        amount=round(0.000225 * face_swap_response['seconds'], 6),
                                        currency=Currency.USD,
                                        quantity=1)

            await send_images(message, images)

            quantity_to_delete = len(images)
            user.monthly_limits[Quota.FACE_SWAP] = max(
                user.monthly_limits[Quota.FACE_SWAP] - quantity_to_delete,
                0,
            )
            user.additional_usage_quota[Quota.FACE_SWAP] = max(
                user.additional_usage_quota[Quota.FACE_SWAP] - quantity_to_delete,
                0,
            )

            await update_user(user.id, {
                "monthly_limits": user.monthly_limits,
                "additional_usage_quota": user.additional_usage_quota,
            })
            await update_face_swap_package(face_swap_package.id, {
                "used_images": face_swap_package.used_images
            })

            await state.clear()
    except ValueError:
        await message.reply(text=get_localization(user.language_code).VALUE_ERROR)
