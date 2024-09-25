import time
import uuid
from typing import List

import aiohttp
from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile, File, ReactionTypeEmoji
from aiogram.utils.chat_action import ChatActionSender

from bot.database.main import firebase
from bot.database.models.common import Model, Quota, ChatGPTVersion, ClaudeGPTVersion, GeminiGPTVersion
from bot.database.models.face_swap_package import FaceSwapPackageStatus
from bot.database.models.user import UserSettings
from bot.database.operations.face_swap_package.getters import (
    get_face_swap_package,
    get_used_face_swap_packages_by_user_id,
)
from bot.database.operations.face_swap_package.updaters import update_face_swap_package, update_used_face_swap_package
from bot.database.operations.generation.writers import write_generation
from bot.database.operations.request.writers import write_request
from bot.database.operations.user.getters import get_user
from bot.handlers.admin.face_swap_handler import handle_manage_face_swap
from bot.handlers.ai.chat_gpt_handler import handle_chatgpt
from bot.handlers.ai.claude_handler import handle_claude
from bot.handlers.ai.face_swap_handler import handle_face_swap
from bot.handlers.ai.gemini_handler import handle_gemini
from bot.integrations.replicateAI import create_face_swap_image
from bot.keyboards.admin.catalog import build_manage_catalog_create_role_confirmation_keyboard
from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.middlewares.AlbumMiddleware import AlbumMiddleware
from bot.states.catalog import Catalog
from bot.states.face_swap import FaceSwap
from bot.states.profile import Profile
from bot.utils.is_already_processing import is_already_processing
from bot.utils.is_messages_limit_exceeded import is_messages_limit_exceeded
from bot.utils.is_time_limit_exceeded import is_time_limit_exceeded

photo_router = Router()
photo_router.message.middleware(AlbumMiddleware())


async def handle_photo(message: Message, state: FSMContext, photo_file: File):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    current_state = await state.get_state()
    if current_state == Profile.waiting_for_photo.state:
        processing_message = await message.reply(text=get_localization(user_language_code).UPLOADING_PHOTO)

        photo_data_io = await message.bot.download_file(photo_file.file_path)
        photo_data = photo_data_io.read()

        blob_path = f'users/avatars/{user_id}.jpeg'
        try:
            blob = await firebase.bucket.get_blob(blob_path)
            await blob.upload(photo_data)
        except aiohttp.ClientResponseError:
            blob = firebase.bucket.new_blob(blob_path)
            await blob.upload(photo_data)

        await message.bot.set_message_reaction(
            message.chat.id,
            message.message_id,
            [ReactionTypeEmoji(emoji='🤩')],
            True,
        )

        used_face_swap_packages = await get_used_face_swap_packages_by_user_id(user_id)
        for used_face_swap_package in used_face_swap_packages:
            await update_used_face_swap_package(used_face_swap_package.id, {
                'used_images': []
            })

        await processing_message.edit_text(get_localization(user_language_code).CHANGE_PHOTO_SUCCESS)

        await state.clear()

        if user.current_model == Model.FACE_SWAP:
            await handle_face_swap(message.bot, str(message.chat.id), state, str(message.from_user.id))
    elif current_state == Catalog.waiting_for_role_photo.state:
        user_data = await state.get_data()

        photo_data_io = await message.bot.download_file(photo_file.file_path)
        photo_data = photo_data_io.read()

        photo_name = f'{user_data["system_role_name"]}.png'
        photo_path = f'roles/{photo_name}'
        photo_blob = firebase.bucket.new_blob(photo_path)
        await photo_blob.upload(photo_data)

        reply_markup = build_manage_catalog_create_role_confirmation_keyboard(user_language_code)
        await message.answer(
            text=get_localization(user_language_code).catalog_manage_create_role_confirmation(
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

        photo_data_io = await message.bot.download_file(photo_file.file_path)
        photo_data = photo_data_io.read()

        face_swap_package = await get_face_swap_package(face_swap_package_id)
        photo_name = f'{len(face_swap_package.files) + 1}_{face_swap_picture_name}.jpeg'
        photo_path = f'face_swap/{user_data["gender"].lower()}/{user_data["package_name"].lower()}/{photo_name}'
        photo_blob = firebase.bucket.new_blob(photo_path)
        await photo_blob.upload(photo_data)
        face_swap_package.files.append({
            'name': photo_name,
            'status': FaceSwapPackageStatus.PRIVATE,
        })

        await update_face_swap_package(
            face_swap_package.id,
            {
                'files': face_swap_package.files
            }
        )

        await message.answer(text=get_localization(user_language_code).FACE_SWAP_MANAGE_EDIT_SUCCESS)
        await handle_manage_face_swap(message, str(message.from_user.id), state)
    elif user.current_model == Model.CHAT_GPT or user.current_model == Model.CLAUDE or user.current_model == Model.GEMINI:
        if user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V4_Omni_Mini:
            quota = Quota.CHAT_GPT4_OMNI_MINI
        elif user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V4_Omni:
            quota = Quota.CHAT_GPT4_OMNI
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Sonnet:
            quota = Quota.CLAUDE_3_SONNET
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Opus:
            quota = Quota.CLAUDE_3_OPUS
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Flash:
            quota = Quota.GEMINI_1_FLASH
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Pro:
            quota = Quota.GEMINI_1_PRO
        else:
            raise NotImplemented(
                f'User quota is not implemented: {user.settings[user.current_model][UserSettings.VERSION]}'
            )

        current_time = time.time()
        need_exit = (
            await is_already_processing(message, state, current_time) or
            await is_messages_limit_exceeded(message, state, user, quota) or
            await is_time_limit_exceeded(message, state, user, current_time)
        )
        if need_exit:
            return

        photo_data_io = await message.bot.download_file(photo_file.file_path)
        photo_data = photo_data_io.read()

        photo_vision_filename = f'{uuid.uuid4()}.jpeg'
        photo_vision_path = f'users/vision/{user_id}/{photo_vision_filename}'
        photo_vision = firebase.bucket.new_blob(photo_vision_path)
        await photo_vision.upload(photo_data)

        if user.current_model == Model.CHAT_GPT:
            await handle_chatgpt(message, state, user, quota, [photo_vision_filename])
        elif user.current_model == Model.CLAUDE:
            await handle_claude(message, state, user, quota, [photo_vision_filename])
        elif user.current_model == Model.GEMINI:
            await handle_gemini(message, state, user, quota, [photo_vision_filename])
    elif user.current_model == Model.FACE_SWAP:
        quota = user.daily_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP]
        quantity = 1
        if quota < quantity:
            await message.answer(text=get_localization(user_language_code).face_swap_package_forbidden(quota))
        else:
            processing_message = await message.reply(
                text=get_localization(user_language_code).processing_request_face_swap()
            )

            async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
                try:
                    user_photo = await firebase.bucket.get_blob(f'users/avatars/{user_id}.jpeg')
                    user_photo_link = firebase.get_public_url(user_photo.name)
                    photo_data_io = await message.bot.download_file(photo_file.file_path)
                    photo_data = photo_data_io.read()

                    background_path = f'users/backgrounds/{user_id}/{uuid.uuid4()}.jpeg'
                    background_photo = firebase.bucket.new_blob(background_path)
                    await background_photo.upload(photo_data)
                    background_photo_link = firebase.get_public_url(background_path)

                    result = await create_face_swap_image(background_photo_link, user_photo_link)
                    request = await write_request(
                        user_id=user_id,
                        message_id=processing_message.message_id,
                        model=Model.FACE_SWAP,
                        requested=1,
                        details={
                            'is_test': False,
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
                    example_photo = await firebase.bucket.get_blob(photo_path)
                    photo_link = firebase.get_public_url(example_photo.name)

                    reply_markup = build_cancel_keyboard(user_language_code)
                    await message.answer_photo(
                        photo=URLInputFile(photo_link, filename=photo_path),
                        caption=get_localization(user_language_code).SEND_ME_YOUR_PICTURE,
                        reply_markup=reply_markup
                    )
                    await state.set_state(Profile.waiting_for_photo)
    else:
        await message.reply(
            text=get_localization(user_language_code).PHOTO_FORBIDDEN_ERROR,
        )


async def handle_album(message: Message, state: FSMContext, album: List[Message]):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.CHAT_GPT or user.current_model == Model.CLAUDE or user.current_model == Model.GEMINI:
        if user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V4_Omni_Mini:
            quota = Quota.CHAT_GPT4_OMNI_MINI
        elif user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V4_Omni:
            quota = Quota.CHAT_GPT4_OMNI
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Sonnet:
            quota = Quota.CLAUDE_3_SONNET
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Opus:
            quota = Quota.CLAUDE_3_OPUS
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Flash:
            quota = Quota.GEMINI_1_FLASH
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Pro:
            quota = Quota.GEMINI_1_PRO
        else:
            raise NotImplemented(
                f'User quota is not implemented: {user.settings[user.current_model][UserSettings.VERSION]}'
            )

        current_time = time.time()
        need_exit = (
            await is_already_processing(message, state, current_time) or
            await is_messages_limit_exceeded(message, state, user, quota) or
            await is_time_limit_exceeded(message, state, user, current_time)
        )
        if need_exit:
            return

        photo_vision_filenames = []
        for file in album:
            if file.photo:
                photo_file = await message.bot.get_file(message.photo[-1].file_id)
            elif file.document.mime_type.startswith('image') and file.document.thumbnail:
                photo_file = await message.bot.get_file(file.document.file_id)
            else:
                continue

            photo_data_io = await message.bot.download_file(photo_file.file_path)
            photo_data = photo_data_io.read()

            photo_vision_filename = f'{uuid.uuid4()}.jpeg'
            photo_vision_path = f'users/vision/{user_id}/{photo_vision_filename}'
            photo_vision = firebase.bucket.new_blob(photo_vision_path)
            await photo_vision.upload(photo_data)

            photo_vision_filenames.append(photo_vision_filename)

        if user.current_model == Model.CHAT_GPT:
            await handle_chatgpt(message, state, user, quota, photo_vision_filenames)
        elif user.current_model == Model.CLAUDE:
            await handle_claude(message, state, user, quota, photo_vision_filenames)
        elif user.current_model == Model.GEMINI:
            await handle_gemini(message, state, user, quota, photo_vision_filenames)
    elif user.current_model == Model.FACE_SWAP:
        await message.reply(
            text=get_localization(user_language_code).ALBUM_FORBIDDEN_ERROR,
        )
    else:
        await message.reply(
            text=get_localization(user_language_code).PHOTO_FORBIDDEN_ERROR,
        )


@photo_router.message(F.photo)
async def photo(message: Message, state: FSMContext, album: List[Message]):
    if len(album):
        await handle_album(message, state, album)
    else:
        photo_file = await message.bot.get_file(message.photo[-1].file_id)
        await handle_photo(message, state, photo_file)
