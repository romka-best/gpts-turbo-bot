import random
import io
from typing import List

from PIL import Image

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from telegram import constants

from bot.database.main import bucket
from bot.database.models.common import Quota, Currency
from bot.database.models.face_swap_package import FaceSwapPackageStatus, FaceSwapFileData
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserGender
from bot.database.operations.face_swap_package import (
    get_used_face_swap_packages_by_user_id,
    get_face_swap_package,
    get_used_face_swap_package_by_user_id_and_package_id,
    get_face_swap_package_by_name_and_gender,
    write_used_face_swap_package, update_used_face_swap_package, get_face_swap_packages)
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


def count_active_files(files_list: List[FaceSwapFileData]) -> int:
    active_count = sum(
        1 for file in files_list if file.get('status', FaceSwapPackageStatus.LEGACY) == FaceSwapPackageStatus.PUBLIC
    )

    return active_count


async def handle_face_swap(message: Message, state: FSMContext, user_id: str):
    user = await get_user(str(user_id))

    if user.gender == UserGender.UNSPECIFIED:
        reply_markup = build_profile_gender_keyboard(user.language_code)
        await message.answer(text=get_localization(user.language_code).TELL_ME_YOUR_GENDER,
                             reply_markup=reply_markup)
    else:
        photo = bucket.blob(f'users/avatars/{user.id}.jpeg')
        if photo.exists():
            used_face_swap_packages = await get_used_face_swap_packages_by_user_id(user.id)
            has_more = False
            for used_face_swap_package in used_face_swap_packages:
                face_swap_package_files = await get_face_swap_package(used_face_swap_package.package_id)
                face_swap_package_quantity = count_active_files(face_swap_package_files.files)
                face_swap_package_used_images = len(used_face_swap_package.used_images)
                remain_images = face_swap_package_quantity - face_swap_package_used_images
                if remain_images > 0:
                    has_more = True
                    break
            if has_more:
                face_swap_packages = await get_face_swap_packages()
                reply_markup = build_face_swap_choose_keyboard(user.language_code, face_swap_packages)
                await message.answer(text=get_localization(user.language_code).CHOOSE_YOUR_PACKAGE,
                                     reply_markup=reply_markup)
            else:
                await message.answer(text=get_localization(user.language_code).GENERATIONS_IN_PACKAGES_ENDED)
        else:
            photo_path = 'users/avatars/example.png'
            photo = bucket.blob(photo_path)
            photo_data = photo.download_as_string()

            await message.answer_photo(
                photo=BufferedInputFile(photo_data, filename=photo_path),
                caption=get_localization(user.language_code).SEND_ME_YOUR_PICTURE
            )
            await state.set_state(Profile.waiting_for_photo)


@face_swap_router.callback_query(lambda c: c.data.startswith('face_swap_choose:'))
async def handle_face_swap_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))
    user_available_images = user.monthly_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP]

    package_name = callback_query.data.split(':')[1]

    face_swap_package = await get_face_swap_package_by_name_and_gender(package_name, user.gender)
    used_face_swap_package = await get_used_face_swap_package_by_user_id_and_package_id(user.id, face_swap_package.id)
    if used_face_swap_package is None:
        used_face_swap_package = await write_used_face_swap_package(user.id, face_swap_package.id, [])
    face_swap_package_quantity = count_active_files(face_swap_package.files)
    face_swap_package_used_images = len(used_face_swap_package.used_images)

    suggested_quantities = set()
    maximum_quantity = user_available_images - face_swap_package_quantity - face_swap_package_used_images
    if maximum_quantity > 0:
        if maximum_quantity // 4 > 0:
            suggested_quantities.add(maximum_quantity // 4)
        if maximum_quantity // 2 > maximum_quantity // 4:
            suggested_quantities.add(maximum_quantity // 2)
        if maximum_quantity > maximum_quantity // 2:
            suggested_quantities.add(maximum_quantity)
    reply_markup = build_face_swap_package_keyboard(user.language_code, sorted(list(suggested_quantities)))

    await callback_query.message.edit_text(
        text=get_localization(user.language_code).choose_face_swap_package(
            name=face_swap_package.translated_names.get(user.language_code, face_swap_package.name),
            available_images=user_available_images,
            total_images=face_swap_package_quantity,
            used_images=face_swap_package_used_images
        ),
        reply_markup=reply_markup)

    await state.set_state(FaceSwap.waiting_for_face_swap_quantity)
    await state.update_data(face_swap_package_name=face_swap_package.name)


@face_swap_router.callback_query(lambda c: c.data.startswith('face_swap_package:'))
async def handle_face_swap_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'cancel':
        await callback_query.delete_message()

        await state.clear()
    elif action == 'back':
        user = await get_user(str(callback_query.from_user.id))

        face_swap_packages = await get_face_swap_packages()
        reply_markup = build_face_swap_choose_keyboard(user.language_code, face_swap_packages)
        await callback_query.message.edit_text(text=get_localization(user.language_code).CHOOSE_YOUR_PACKAGE,
                                               reply_markup=reply_markup)

        await state.clear()
    else:
        await face_swap_quantity_handler(callback_query.message, state, str(callback_query.from_user.id), action)


async def face_swap_quantity_handler(message: Message, state: FSMContext, user_id: str, chosen_quantity: str):
    user = await get_user(str(user_id))
    user_data = await state.get_data()

    processing_message = await message.reply(
        text=get_localization(user.language_code).processing_request_face_swap()
    )

    try:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.UPLOAD_PHOTO)

        quota = user.monthly_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP]
        quantity = int(chosen_quantity)
        name = user_data['face_swap_package_name']
        face_swap_package = await get_face_swap_package_by_name_and_gender(name, user.gender)
        face_swap_package_quantity = count_active_files(face_swap_package.files)

        if quota < quantity:
            await message.answer(text=get_localization(user.language_code).face_swap_package_forbidden(quota))
        elif quantity < 1:
            await message.answer(text=get_localization(user.language_code).FACE_SWAP_MIN_ERROR)
        elif face_swap_package_quantity < quantity:
            await message.answer(text=get_localization(user.language_code).FACE_SWAP_MAX_ERROR)
        else:
            user_photo = bucket.blob(f'users/avatars/{user.id}.jpeg')
            user_photo.make_public()
            user_photo_link = user_photo.public_url
            used_face_swap_package = await get_used_face_swap_package_by_user_id_and_package_id(user.id,
                                                                                                face_swap_package.id)
            images = []
            for _ in range(quantity):
                random_image_name = random.choice(face_swap_package.files)['name']
                while random_image_name in used_face_swap_package.used_images:
                    random_image_name = random.choice(face_swap_package.files)['name']
                used_face_swap_package.used_images.append(random_image_name)

                random_image = bucket.blob(
                    f'face_swap/{user.gender.lower()}/{face_swap_package.name.lower()}/{random_image_name}'
                )
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
            await update_used_face_swap_package(face_swap_package.id, {
                "used_images": used_face_swap_package.used_images
            })

            await state.clear()
    except ValueError:
        await message.reply(text=get_localization(user.language_code).VALUE_ERROR)
    finally:
        await processing_message.delete()


@face_swap_router.message(FaceSwap.waiting_for_face_swap_quantity)
async def face_swap_quantity_sent(message: Message, state: FSMContext):
    await face_swap_quantity_handler(message, state, str(message.from_user.id), message.text)
