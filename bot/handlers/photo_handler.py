import uuid

import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from aiogram.utils.chat_action import ChatActionSender

from bot.database.main import firebase
from bot.database.models.common import Model, Quota
from bot.database.models.face_swap_package import FaceSwapPackageStatus
from bot.database.operations.face_swap_package import (
    get_used_face_swap_packages_by_user_id,
    update_used_face_swap_package,
    get_face_swap_package,
    update_face_swap_package,
)
from bot.database.operations.generation import write_generation
from bot.database.operations.request import write_request
from bot.database.operations.user import get_user
from bot.handlers.face_swap_handler import handle_face_swap
from bot.integrations.replicateAI import create_face_swap_image
from bot.keyboards.catalog import build_manage_catalog_create_role_confirmation_keyboard
from bot.keyboards.common import build_cancel_keyboard
from bot.locales.main import get_localization
from bot.states.catalog import Catalog
from bot.states.face_swap import FaceSwap
from bot.states.profile import Profile

photo_router = Router()


@photo_router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    current_state = await state.get_state()
    if current_state == Profile.waiting_for_photo.state:
        photo = message.photo[-1]
        photo_file = await message.bot.get_file(photo.file_id)
        photo_data_io = await message.bot.download_file(photo_file.file_path)
        photo_data = photo_data_io.read()

        blob_path = f"users/avatars/{user.id}.jpeg"
        try:
            blob = await firebase.bucket.get_blob(blob_path)
            await blob.upload(photo_data)
        except Exception:
            blob = firebase.bucket.new_blob(blob_path)
            await blob.upload(photo_data)

        used_face_swap_packages = await get_used_face_swap_packages_by_user_id(user.id)
        for used_face_swap_package in used_face_swap_packages:
            await update_used_face_swap_package(used_face_swap_package.id, {
                "used_images": []
            })

        await message.reply(get_localization(user.language_code).CHANGE_PHOTO_SUCCESS)

        await state.clear()

        if user.current_model == Model.FACE_SWAP:
            await handle_face_swap(message.bot, str(message.chat.id), state, str(message.from_user.id))
    elif current_state == Catalog.waiting_for_role_photo.state:
        user_data = await state.get_data()

        photo = message.photo[-1]
        photo_file = await message.bot.get_file(photo.file_id)
        photo_data_io = await message.bot.download_file(photo_file.file_path)
        photo_data = photo_data_io.read()

        photo_name = f'{user_data["system_role_name"]}.png'
        photo_path = f'roles/{photo_name}'
        photo_blob = firebase.bucket.new_blob(photo_path)
        await photo_blob.upload(photo_data)

        reply_markup = build_manage_catalog_create_role_confirmation_keyboard(user.language_code)
        await message.answer(
            text=get_localization(user.language_code).catalog_manage_create_role_confirmation(
                role_system_name=user_data.get('system_role_name', None),
                role_names=user_data.get('role_names', {}),
                role_descriptions=user_data.get('role_descriptions', {}),
                role_instructions=user_data.get('role_instructions', {}),
            ),
            reply_markup=reply_markup,
        )
    elif current_state == FaceSwap.waiting_for_face_swap_picture_image.state:
        user_data = await state.get_data()
        face_swap_package_id = user_data['face_swap_package_id']
        face_swap_picture_name = user_data['face_swap_picture_name']

        photo = message.photo[-1]
        photo_file = await message.bot.get_file(photo.file_id)
        photo_data_io = await message.bot.download_file(photo_file.file_path)
        photo_data = photo_data_io.read()

        face_swap_package = await get_face_swap_package(face_swap_package_id)
        photo_name = f'{len(face_swap_package.files) + 1}_{face_swap_picture_name}.jpeg'
        photo_path = f'face_swap/{user_data["gender"].lower()}/{user_data["package_name"].lower()}/{photo_name}'
        photo_blob = firebase.bucket.new_blob(photo_path)
        await photo_blob.upload(photo_data)
        face_swap_package.files.append({
            "name": photo_name,
            "status": FaceSwapPackageStatus.PRIVATE,
        })

        await update_face_swap_package(
            face_swap_package.id,
            {
                'files': face_swap_package.files
            }
        )

        await message.answer(text=get_localization(user.language_code).FACE_SWAP_MANAGE_EDIT_SUCCESS)
    elif user.current_model == Model.FACE_SWAP:
        quota = user.monthly_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP]
        quantity = 1
        if quota < quantity:
            await message.answer(text=get_localization(user.language_code).face_swap_package_forbidden(quota))
        else:
            processing_message = await message.reply(
                text=get_localization(user.language_code).processing_request_face_swap()
            )

            async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
                try:
                    user_photo = await firebase.bucket.get_blob(f'users/avatars/{user.id}.jpeg')
                    user_photo_link = firebase.get_public_url(user_photo.name)
                    photo = message.photo[-1]
                    photo_file = await message.bot.get_file(photo.file_id)
                    photo_data_io = await message.bot.download_file(photo_file.file_path)
                    photo_data = photo_data_io.read()

                    background_path = f"users/backgrounds/{user.id}/{uuid.uuid4()}.jpeg"
                    background_photo = firebase.bucket.new_blob(background_path)
                    await background_photo.upload(photo_data)
                    background_photo_link = firebase.get_public_url(background_path)

                    result = await create_face_swap_image(background_photo_link, user_photo_link)
                    request = await write_request(
                        user_id=user.id,
                        message_id=processing_message.message_id,
                        model=Model.FACE_SWAP,
                        requested=1,
                        details={
                            "is_test": False,
                        }
                    )
                    await write_generation(
                        id=result,
                        request_id=request.id,
                        model=Model.FACE_SWAP,
                        has_error=result is None
                    )

                    await state.clear()
                except aiohttp.ClientResponseError:
                    photo_path = 'users/avatars/example.png'
                    photo = await firebase.bucket.get_blob(photo_path)
                    photo_link = firebase.get_public_url(photo.name)

                    reply_markup = build_cancel_keyboard(user.language_code)
                    await message.answer_photo(
                        photo=URLInputFile(photo_link, filename=photo_path),
                        caption=get_localization(user.language_code).SEND_ME_YOUR_PICTURE,
                        reply_markup=reply_markup
                    )
                    await state.set_state(Profile.waiting_for_photo)
