import io
import uuid

from PIL import Image
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.main import bucket
from bot.database.models.common import Model, Quota, Currency
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserGender
from bot.database.operations.face_swap_package import update_face_swap_package, get_face_swap_packages_by_user_id
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user, update_user
from bot.handlers.face_swap_handler import handle_face_swap
from bot.helpers.send_images import send_images
from bot.integrations.replicateAI import get_face_swap_image
from bot.locales.main import get_localization
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

        blob = bucket.blob(f"users/avatars/{user.id}.jpeg")
        blob.upload_from_string(photo_data, content_type='image/jpeg')

        face_swap_packages = await get_face_swap_packages_by_user_id(user.id)
        for face_swap_package in face_swap_packages:
            await update_face_swap_package(face_swap_package.id, {
                UserGender.MALE: [],
                UserGender.FEMALE: []
            })

        await message.reply(get_localization(user.language_code).CHANGE_PHOTO_SUCCESS)

        await state.clear()

        if user.current_model == Model.FACE_SWAP:
            await handle_face_swap(message, state, str(message.from_user.id))
    elif user.current_model == Model.FACE_SWAP:
        quota = user.monthly_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP]
        quantity = len(message.photo)
        if quota < quantity:
            await message.answer(text=get_localization(user.language_code).face_swap_package_forbidden(quota))
        else:
            user_photo = bucket.blob(f'users/avatars/{user.id}.jpeg')
            user_photo.make_public()
            user_photo_link = user_photo.public_url
            images = []
            for photo in message.photo:
                photo_file = await message.bot.get_file(photo.file_id)
                photo_data_io = await message.bot.download_file(photo_file.file_path)
                photo_data = photo_data_io.read()

                background_photo = bucket.blob(f"users/backgrounds/{user.id}/{uuid.uuid4()}.jpeg")
                background_photo.upload_from_string(photo_data, content_type='image/jpeg')
                background_photo.make_public()
                background_photo_link = background_photo.public_url
                background_photo_data = background_photo.download_as_bytes()
                image = Image.open(io.BytesIO(background_photo_data))

                width, height = image.size

                face_swap_response = await get_face_swap_image(width, height, background_photo_link, user_photo_link)
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

            await state.clear()
