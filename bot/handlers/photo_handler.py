import asyncio
import uuid

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile

from bot.database.main import firebase
from bot.database.models.common import Model, Quota, Currency
from bot.database.models.face_swap_package import FaceSwapPackageStatus
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.face_swap_package import get_used_face_swap_packages_by_user_id, \
    update_used_face_swap_package, get_face_swap_package, update_face_swap_package
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user, update_user
from bot.handlers.face_swap_handler import handle_face_swap, PRICE_FACE_SWAP
from bot.integrations.replicateAI import get_face_swap_image
from bot.locales.main import get_localization
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
            await handle_face_swap(message, state, str(message.from_user.id))
    elif current_state == FaceSwap.waiting_for_face_swap_picture.state:
        user_data = await state.get_data()

        photo = message.photo[-1]
        photo_file = await message.bot.get_file(photo.file_id)
        photo_data_io = await message.bot.download_file(photo_file.file_path)
        photo_data = photo_data_io.read()

        face_swap_package = await get_face_swap_package(user_data['face_swap_package_id'])
        photo_name = f'{len(face_swap_package.files) + 1}_{uuid.uuid4()}.jpeg'
        photo_path = f'face_swap/{user_data["gender"].lower()}/{user_data["package_name"].lower()}/{photo_name}'
        photo_bolb = firebase.bucket.new_blob(photo_path)
        await photo_bolb.upload(photo_data)
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
        quantity = len(message.photo)
        if quota < quantity:
            await message.answer(text=get_localization(user.language_code).face_swap_package_forbidden(quota))
        else:
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

            result = await get_face_swap_image(background_photo_link, user_photo_link)
            await message.reply_photo(
                photo=URLInputFile(result['image'], filename=background_path),
            )

            quantity_to_delete = 1
            user.monthly_limits[Quota.FACE_SWAP] = max(
                user.monthly_limits[Quota.FACE_SWAP] - quantity_to_delete,
                0,
            )
            user.additional_usage_quota[Quota.FACE_SWAP] = max(
                user.additional_usage_quota[Quota.FACE_SWAP] - quantity_to_delete,
                0,
            )

            update_tasks = [
                write_transaction(user_id=user.id, type=TransactionType.EXPENSE, service=ServiceType.FACE_SWAP,
                                  amount=round(PRICE_FACE_SWAP * result['seconds'], 6), currency=Currency.USD,
                                  quantity=quantity),
                update_user(user.id, {
                    "monthly_limits": user.monthly_limits,
                    "additional_usage_quota": user.additional_usage_quota
                }),
            ]
            await asyncio.gather(*update_tasks)

            await handle_face_swap(message, state, user.id)

            await state.clear()
