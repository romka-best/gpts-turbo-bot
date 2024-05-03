import asyncio
import random
from typing import List

import aiohttp
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    URLInputFile,
)
from aiogram.utils.chat_action import ChatActionSender

from bot.database.main import firebase
from bot.database.models.common import Quota, Model
from bot.database.models.face_swap_package import (
    FaceSwapPackage,
    FaceSwapPackageStatus,
    FaceSwapFileData,
    UsedFaceSwapPackage,
)
from bot.database.models.generation import GenerationStatus
from bot.database.models.request import RequestStatus
from bot.database.models.user import UserGender, User
from bot.database.operations.face_swap_package.getters import (
    get_face_swap_package,
    get_face_swap_packages_by_gender,
    get_face_swap_package_by_name_and_gender,
    get_used_face_swap_packages_by_user_id,
    get_used_face_swap_package_by_user_id_and_package_id,
)
from bot.database.operations.face_swap_package.writers import write_used_face_swap_package
from bot.database.operations.generation.getters import get_generations_by_request_id
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.generation.writers import write_generation
from bot.database.operations.request.getters import get_started_requests_by_user_id_and_model
from bot.database.operations.request.updaters import update_request
from bot.database.operations.request.writers import write_request
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.integrations.replicateAI import create_face_swap_images
from bot.keyboards.ai.face_swap import (
    build_face_swap_choose_keyboard,
    build_face_swap_package_keyboard,
)
from bot.keyboards.common.common import build_cancel_keyboard, build_recommendations_keyboard
from bot.keyboards.common.profile import build_profile_gender_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.face_swap import FaceSwap
from bot.states.profile import Profile

face_swap_router = Router()

PRICE_FACE_SWAP = 0.000725


def count_active_files(files_list: List[FaceSwapFileData]) -> int:
    active_count = sum(
        1 for file in files_list if file.get('status', FaceSwapPackageStatus.LEGACY) == FaceSwapPackageStatus.PUBLIC
    )

    return active_count


@face_swap_router.message(Command("face_swap"))
async def face_swap(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.FACE_SWAP:
        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        user.current_model = Model.FACE_SWAP
        await update_user(user_id, {
            "current_model": user.current_model,
        })

        reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
        await message.answer(
            text=get_localization(user_language_code).SWITCHED_TO_FACE_SWAP,
            reply_markup=reply_markup,
        )

    await handle_face_swap(message.bot, user.telegram_chat_id, state, user_id)


async def handle_face_swap(bot: Bot, chat_id: str, state: FSMContext, user_id: str, chosen_package=None):
    user = await get_user(str(user_id))
    user_language_code = await get_user_language(str(user_id), state.storage)

    if user.gender == UserGender.UNSPECIFIED:
        reply_markup = build_profile_gender_keyboard(user_language_code)
        await bot.send_message(
            chat_id=chat_id,
            text=get_localization(user_language_code).TELL_ME_YOUR_GENDER,
            reply_markup=reply_markup,
        )
    else:
        try:
            await firebase.bucket.get_blob(f'users/avatars/{user_id}.jpeg')

            used_face_swap_packages = await get_used_face_swap_packages_by_user_id(user_id)
            face_swap_packages = await get_face_swap_packages_by_gender(
                user.gender,
                status=FaceSwapPackageStatus.PUBLIC,
            )
            has_more = False
            for used_face_swap_package in used_face_swap_packages:
                face_swap_package_files = await get_face_swap_package(used_face_swap_package.package_id)
                face_swap_package_quantity = count_active_files(face_swap_package_files.files)
                face_swap_package_used_images = len(used_face_swap_package.used_images)
                remain_images = face_swap_package_quantity - face_swap_package_used_images
                if remain_images > 0:
                    has_more = True
                    break
            if has_more or not used_face_swap_packages or len(face_swap_packages) > len(used_face_swap_packages):
                face_swap_packages = await get_face_swap_packages_by_gender(
                    gender=user.gender,
                    status=FaceSwapPackageStatus.PUBLIC,
                )
                chosen_package = next(
                    (
                        face_swap_package for face_swap_package in face_swap_packages if
                        face_swap_package.translated_names.get(user_language_code) == chosen_package
                    ),
                    None,
                ) if chosen_package else None
                if chosen_package:
                    await handle_face_swap_choose_selection(bot, chat_id, 0, user, chosen_package.name, state)
                else:
                    reply_markup = build_face_swap_choose_keyboard(user_language_code, face_swap_packages)
                    await bot.send_message(
                        chat_id=chat_id,
                        text=get_localization(user_language_code).CHOOSE_YOUR_PACKAGE,
                        reply_markup=reply_markup,
                    )
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=get_localization(user_language_code).GENERATIONS_IN_PACKAGES_ENDED,
                )
        except aiohttp.ClientResponseError:
            photo_path = 'users/avatars/example.png'
            photo = await firebase.bucket.get_blob(photo_path)
            photo_link = firebase.get_public_url(photo.name)

            reply_markup = build_cancel_keyboard(user_language_code)
            await bot.send_photo(
                chat_id=chat_id,
                photo=URLInputFile(photo_link, filename=photo_path),
                caption=get_localization(user_language_code).SEND_ME_YOUR_PICTURE,
                reply_markup=reply_markup
            )
            await state.set_state(Profile.waiting_for_photo)


async def handle_face_swap_choose_selection(
    bot: Bot,
    chat_id: str,
    message_id: int,
    user: User,
    package_name: str,
    state: FSMContext,
):
    user_language_code = await get_user_language(user.id, state.storage)
    user_available_images = user.monthly_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP]

    face_swap_package = await get_face_swap_package_by_name_and_gender(package_name, user.gender)
    used_face_swap_package = await get_used_face_swap_package_by_user_id_and_package_id(user.id, face_swap_package.id)
    if used_face_swap_package is None:
        used_face_swap_package = await write_used_face_swap_package(user.id, face_swap_package.id, [])
    face_swap_package_quantity = count_active_files(face_swap_package.files)
    face_swap_package_used_images = len(used_face_swap_package.used_images)

    suggested_quantities = set()
    maximum_quantity = face_swap_package_quantity - face_swap_package_used_images
    if maximum_quantity > 0:
        if maximum_quantity // 4 > 0:
            suggested_quantities.add(maximum_quantity // 4)
        if maximum_quantity // 2 > maximum_quantity // 4:
            suggested_quantities.add(maximum_quantity // 2)
        if maximum_quantity > maximum_quantity // 2:
            suggested_quantities.add(maximum_quantity)
    reply_markup = build_face_swap_package_keyboard(user_language_code, sorted(list(suggested_quantities)))

    if message_id != 0:
        await bot.edit_message_text(
            text=get_localization(user_language_code).choose_face_swap_package(
                name=face_swap_package.translated_names.get(user_language_code, face_swap_package.name),
                available_images=user_available_images,
                total_images=face_swap_package_quantity,
                used_images=face_swap_package_used_images
            ),
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        )
    else:
        await bot.send_message(
            text=get_localization(user_language_code).choose_face_swap_package(
                name=face_swap_package.translated_names.get(user_language_code, face_swap_package.name),
                available_images=user_available_images,
                total_images=face_swap_package_quantity,
                used_images=face_swap_package_used_images
            ),
            chat_id=chat_id,
            reply_markup=reply_markup,
        )

    await state.update_data(face_swap_package_name=face_swap_package.name)
    await state.update_data(maximum_quantity=maximum_quantity)
    if maximum_quantity > 0:
        await state.set_state(FaceSwap.waiting_for_face_swap_quantity)


@face_swap_router.callback_query(lambda c: c.data.startswith('face_swap_choose:'))
async def face_swap_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))
    package_name = callback_query.data.split(':')[1]
    await handle_face_swap_choose_selection(
        callback_query.message.bot,
        str(callback_query.message.chat.id),
        callback_query.message.message_id,
        user,
        package_name,
        state,
    )


@face_swap_router.callback_query(lambda c: c.data.startswith('face_swap_package:'))
async def handle_face_swap_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    action = callback_query.data.split(':')[1]

    if action == 'back':
        user = await get_user(user_id)
        user_language_code = await get_user_language(user_id, state.storage)

        face_swap_packages = await get_face_swap_packages_by_gender(
            gender=user.gender,
            status=FaceSwapPackageStatus.PUBLIC,
        )
        reply_markup = build_face_swap_choose_keyboard(user_language_code, face_swap_packages)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).CHOOSE_YOUR_PACKAGE,
            reply_markup=reply_markup
        )

        await state.clear()
    else:
        await face_swap_quantity_handler(callback_query.message, state, user_id, action)


def select_unique_images(
    face_swap_package: FaceSwapPackage,
    used_face_swap_package: UsedFaceSwapPackage,
    quantity: int,
):
    unique_images = []

    available_images = [
        file for file in face_swap_package.files if file['name'] not in used_face_swap_package.used_images
    ]

    while len(unique_images) < quantity and available_images:
        selected_image = random.choice(available_images)
        unique_images.append(selected_image['name'])
        available_images.remove(selected_image)
        used_face_swap_package.used_images.append(selected_image['name'])

    return unique_images


async def generate_face_swap_images(
    quantity: int,
    gender: str,
    face_swap_package: FaceSwapPackage,
    used_face_swap_package: UsedFaceSwapPackage,
    user_photo_link: str
):
    random_names = select_unique_images(face_swap_package, used_face_swap_package, quantity)
    random_images = [
        {
            'target_image': firebase.get_public_url(
                f'face_swap/{gender}/{face_swap_package.name.lower()}/{random_names[i]}'
            ),
            'source_image': user_photo_link,
        } for i in range(quantity)
    ]

    results = await create_face_swap_images(random_images)
    return results, random_names


async def face_swap_quantity_handler(message: Message, state: FSMContext, user_id: str, chosen_quantity: str):
    user = await get_user(str(user_id))
    user_language_code = await get_user_language(str(user_id), state.storage)
    user_data = await state.get_data()

    processing_message = await message.reply(
        text=get_localization(user_language_code).processing_request_face_swap()
    )

    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        quota = user.monthly_limits[Quota.FACE_SWAP] + user.additional_usage_quota[Quota.FACE_SWAP]
        quantity = int(chosen_quantity)
        name = user_data.get('face_swap_package_name')
        face_swap_package_quantity = user_data.get('maximum_quantity')
        if not name or not face_swap_package_quantity:
            await handle_face_swap(message.bot, user.telegram_chat_id, state, user_id)

            await processing_message.delete()
            await message.delete()
            return

        face_swap_package = await get_face_swap_package_by_name_and_gender(name, user.gender)

        if quota < quantity:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).face_swap_package_forbidden(quota),
                reply_markup=reply_markup,
            )
        elif quantity < 1:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).FACE_SWAP_MIN_ERROR,
                reply_markup=reply_markup,
            )
        elif face_swap_package_quantity < quantity:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).FACE_SWAP_MAX_ERROR,
                reply_markup=reply_markup,
            )
        else:
            user_not_finished_requests = await get_started_requests_by_user_id_and_model(user.id, Model.FACE_SWAP)

            if len(user_not_finished_requests):
                await message.reply(
                    text=get_localization(user_language_code).ALREADY_MAKE_REQUEST,
                )
                await processing_message.delete()
                return

            user_photo = await firebase.bucket.get_blob(f'users/avatars/{user.id}.jpeg')
            user_photo_link = firebase.get_public_url(user_photo.name)
            used_face_swap_package = await get_used_face_swap_package_by_user_id_and_package_id(
                user.id,
                face_swap_package.id,
            )

            request = await write_request(
                user_id=user.id,
                message_id=processing_message.message_id,
                model=Model.FACE_SWAP,
                requested=quantity,
                details={
                    "is_test": False,
                    "face_swap_package_id": face_swap_package.id,
                    "face_swap_package_name": face_swap_package.name,
                },
            )

            try:
                results, random_names = await generate_face_swap_images(
                    quantity,
                    user.gender.lower(),
                    face_swap_package,
                    used_face_swap_package,
                    user_photo_link,
                )
                tasks = []
                for (i, result) in enumerate(results):
                    if result is not None:
                        tasks.append(
                            write_generation(
                                id=result,
                                request_id=request.id,
                                model=Model.FACE_SWAP,
                                has_error=result is None,
                                details={
                                    "used_face_swap_package_id": used_face_swap_package.id,
                                    "used_face_swap_package_used_image": random_names[i],
                                }
                            )
                        )
                await asyncio.gather(*tasks)

                await state.update_data(maximum_quantity=face_swap_package_quantity - quantity)
            except (TypeError, ValueError):
                reply_markup = build_cancel_keyboard(user_language_code)
                await message.reply(
                    text=get_localization(user_language_code).VALUE_ERROR,
                    reply_markup=reply_markup,
                )

                await processing_message.delete()
            except Exception as e:
                await message.answer(
                    text=get_localization(user_language_code).ERROR,
                    parse_mode=None,
                )
                await send_message_to_admins(
                    bot=message.bot,
                    message=f"#error\n\nALARM! Ошибка у пользователя при запросе в FaceSwap: {user.id}\nИнформация:\n{e}",
                    parse_mode=None,
                )

                request.status = RequestStatus.FINISHED
                await update_request(request.id, {
                    "status": request.status
                })

                generations = await get_generations_by_request_id(request.id)
                for generation in generations:
                    generation.status = GenerationStatus.FINISHED,
                    generation.has_error = True
                    await update_generation(
                        generation.id,
                        {
                            "status": generation.status,
                            "has_error": generation.has_error,
                        },
                    )


@face_swap_router.message(FaceSwap.waiting_for_face_swap_quantity, ~F.text.startswith('/'))
async def face_swap_quantity_sent(message: Message, state: FSMContext):
    await face_swap_quantity_handler(message, state, str(message.from_user.id), message.text)
