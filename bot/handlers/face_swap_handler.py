import asyncio
import random
from typing import List, Dict

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardButton, InlineKeyboardMarkup, \
    URLInputFile
from telegram import constants

from bot.database.main import firebase
from bot.database.models.common import Quota, Currency
from bot.database.models.face_swap_package import FaceSwapPackageStatus, FaceSwapFileData, FaceSwapPackage, \
    UsedFaceSwapPackage
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserGender
from bot.database.operations.face_swap_package import (
    get_used_face_swap_packages_by_user_id,
    get_face_swap_package,
    get_used_face_swap_package_by_user_id_and_package_id,
    get_face_swap_package_by_name_and_gender,
    write_used_face_swap_package,
    update_used_face_swap_package,
    write_face_swap_package,
    update_face_swap_package,
    get_face_swap_packages_by_gender)
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user, update_user
from bot.helpers.send_images import send_images
from bot.helpers.translate_text import translate_text
from bot.integrations.replicateAI import get_face_swap_image, get_face_swap_images
from bot.keyboards.common import build_cancel_keyboard
from bot.keyboards.face_swap import (
    build_face_swap_choose_keyboard,
    build_face_swap_package_keyboard,
    build_manage_face_swap_keyboard,
    build_manage_face_swap_create_keyboard,
    build_manage_face_swap_create_package_name_keyboard,
    build_manage_face_swap_create_confirmation_keyboard,
    build_manage_face_swap_edit_keyboard,
    build_manage_face_swap_edit_package_change_status_keyboard,
    build_manage_face_swap_edit_choose_gender_keyboard,
    build_manage_face_swap_edit_picture_keyboard,
    build_manage_face_swap_add_picture_keyboard,
    build_manage_face_swap_edit_picture_change_status_keyboard,
    build_manage_face_swap_edit_choose_package_keyboard)
from bot.keyboards.profile import build_profile_gender_keyboard
from bot.locales.main import get_localization, localization_classes
from bot.states.face_swap import FaceSwap
from bot.states.profile import Profile
from bot.utils.is_admin import is_admin

face_swap_router = Router()

PRICE_FACE_SWAP = 0.000225


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
        photo = await firebase.bucket.get_blob(f'users/avatars/{user.id}.jpeg')
        try:
            used_face_swap_packages = await get_used_face_swap_packages_by_user_id(user.id)
            face_swap_packages = await get_face_swap_packages_by_gender(user.gender,
                                                                        status=FaceSwapPackageStatus.PUBLIC)
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
                reply_markup = build_face_swap_choose_keyboard(user.language_code, face_swap_packages)
                await message.answer(text=get_localization(user.language_code).CHOOSE_YOUR_PACKAGE,
                                     reply_markup=reply_markup)
            else:
                await message.answer(text=get_localization(user.language_code).GENERATIONS_IN_PACKAGES_ENDED)
        except Exception:
            photo_path = 'users/avatars/example.png'
            photo = await firebase.bucket.get_blob(photo_path)
            photo_data = await photo.download()

            reply_markup = build_cancel_keyboard(user.language_code)
            await message.answer_photo(
                photo=BufferedInputFile(photo_data, filename=photo_path),
                caption=get_localization(user.language_code).SEND_ME_YOUR_PICTURE,
                reply_markup=reply_markup
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
    maximum_quantity = face_swap_package_quantity - face_swap_package_used_images
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

    if action == 'back':
        user = await get_user(str(callback_query.from_user.id))

        face_swap_packages = await get_face_swap_packages_by_gender(
            gender=user.gender,
            status=FaceSwapPackageStatus.PUBLIC,
        )
        reply_markup = build_face_swap_choose_keyboard(user.language_code, face_swap_packages)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).CHOOSE_YOUR_PACKAGE,
            reply_markup=reply_markup
        )

        await state.clear()
    else:
        await face_swap_quantity_handler(callback_query.message, state, str(callback_query.from_user.id), action)


def select_unique_images(face_swap_package: FaceSwapPackage,
                         used_face_swap_package: UsedFaceSwapPackage,
                         quantity: int):
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

    results = await get_face_swap_images(random_images)
    return results


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
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.answer(text=get_localization(user.language_code).face_swap_package_forbidden(quota),
                                 reply_markup=reply_markup)
        elif quantity < 1:
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.answer(text=get_localization(user.language_code).FACE_SWAP_MIN_ERROR,
                                 reply_markup=reply_markup)
        elif face_swap_package_quantity < quantity:
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.answer(text=get_localization(user.language_code).FACE_SWAP_MAX_ERROR,
                                 reply_markup=reply_markup)
        else:
            user_photo = await firebase.bucket.get_blob(f'users/avatars/{user.id}.jpeg')
            user_photo_link = firebase.get_public_url(user_photo.name)
            used_face_swap_package = await get_used_face_swap_package_by_user_id_and_package_id(user.id,
                                                                                                face_swap_package.id)

            results = await generate_face_swap_images(quantity,
                                                      user.gender.lower(),
                                                      face_swap_package,
                                                      used_face_swap_package,
                                                      user_photo_link)

            images = []
            for result in results:
                if result['image'] is not None:
                    images.append(result['image'])
            total_seconds = sum(result['seconds'] for result in results)

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

            update_tasks = [
                write_transaction(user_id=user.id, type=TransactionType.EXPENSE, service=ServiceType.FACE_SWAP,
                                  amount=round(PRICE_FACE_SWAP * total_seconds, 6), currency=Currency.USD,
                                  quantity=quantity),
                update_user(user.id, {
                    "monthly_limits": user.monthly_limits,
                    "additional_usage_quota": user.additional_usage_quota
                }),
                update_used_face_swap_package(used_face_swap_package.id, {
                    "used_images": used_face_swap_package.used_images
                })
            ]
            await asyncio.gather(*update_tasks)

            await handle_face_swap(message, state, user.id)

            await state.clear()
    except ValueError:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(text=get_localization(user.language_code).VALUE_ERROR,
                            reply_markup=reply_markup)
    finally:
        await processing_message.delete()


@face_swap_router.message(FaceSwap.waiting_for_face_swap_quantity)
async def face_swap_quantity_sent(message: Message, state: FSMContext):
    await face_swap_quantity_handler(message, state, str(message.from_user.id), message.text)


# Admin
async def handle_manage_face_swap(message: Message, user_id: str):
    if is_admin(str(message.chat.id)):
        user = await get_user(str(user_id))

        reply_markup = build_manage_face_swap_keyboard(user.language_code)

        await message.answer(text=get_localization(user.language_code).FACE_SWAP_MANAGE,
                             reply_markup=reply_markup)


@face_swap_router.message(Command("manage_face_swap"))
async def manage_face_swap(message: Message, state: FSMContext):
    await state.clear()

    await handle_manage_face_swap(message, str(message.from_user.id))


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm:'))
async def handle_face_swap_manage_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    action = callback_query.data.split(':')[1]

    if action == 'create':
        reply_markup = build_manage_face_swap_create_keyboard(user.language_code)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).FACE_SWAP_MANAGE_CREATE,
            reply_markup=reply_markup,
        )

        await state.set_state(FaceSwap.waiting_for_face_swap_system_package_name)
    elif action == 'edit':
        reply_markup = build_manage_face_swap_edit_choose_gender_keyboard(user.language_code)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).FACE_SWAP_MANAGE_EDIT_CHOOSE_GENDER,
            reply_markup=reply_markup,
        )


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm_create:'))
async def handle_face_swap_manage_create_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'back':
        await handle_manage_face_swap(callback_query.message, str(callback_query.from_user.id))

        await callback_query.message.delete()

        await state.clear()


@face_swap_router.message(FaceSwap.waiting_for_face_swap_system_package_name)
async def face_swap_manage_system_name_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    system_face_swap_package_name = message.text.upper()
    face_swap_package_male = await get_face_swap_package_by_name_and_gender(system_face_swap_package_name,
                                                                            UserGender.MALE)
    face_swap_package_female = await get_face_swap_package_by_name_and_gender(system_face_swap_package_name,
                                                                              UserGender.FEMALE)
    if face_swap_package_male or face_swap_package_female:
        await message.answer(
            text=get_localization(user.language_code).FACE_SWAP_MANAGE_CREATE_ALREADY_EXISTS_ERROR,
        )
    else:
        reply_markup = build_manage_face_swap_create_package_name_keyboard(user.language_code)
        await message.answer(
            text=get_localization(user.language_code).FACE_SWAP_MANAGE_CREATE_PACKAGE_NAME,
            reply_markup=reply_markup,
        )

        await state.update_data(system_face_swap_package_name=system_face_swap_package_name)
        await state.set_state(FaceSwap.waiting_for_face_swap_package_name)


@face_swap_router.message(FaceSwap.waiting_for_face_swap_package_name)
async def face_swap_manage_name_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))
    user_data = await state.get_data()

    face_swap_package_names = {}
    for language_code in localization_classes.keys():
        if language_code == 'ru':
            face_swap_package_names[language_code] = message.text
        else:
            translated_face_swap_package_name = await translate_text(message.text, 'ru', language_code)
            if translated_face_swap_package_name:
                face_swap_package_names[language_code] = translated_face_swap_package_name
            else:
                face_swap_package_names[language_code] = message.text

    reply_markup = build_manage_face_swap_create_confirmation_keyboard(user.language_code)
    await message.answer(
        text=get_localization(user.language_code).face_swap_manage_create_package_confirmation(
            package_system_name=user_data['system_face_swap_package_name'],
            package_names=face_swap_package_names,
        ),
        reply_markup=reply_markup,
    )

    await state.update_data(face_swap_package_names=face_swap_package_names)


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm_create_confirmation:'))
async def handle_face_swap_manage_create_confirmation_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'approve':
        user = await get_user(str(callback_query.from_user.id))
        user_data = await state.get_data()

        await write_face_swap_package(
            name=user_data['system_face_swap_package_name'],
            translated_names=user_data['face_swap_package_names'],
            gender=UserGender.MALE,
            files=[],
            status=FaceSwapPackageStatus.PRIVATE,
        )
        await write_face_swap_package(
            name=user_data['system_face_swap_package_name'],
            translated_names=user_data['face_swap_package_names'],
            gender=UserGender.FEMALE,
            files=[],
            status=FaceSwapPackageStatus.PRIVATE,
        )

        await callback_query.message.answer(text=get_localization(user.language_code).FACE_SWAP_MANAGE_CREATE_SUCCESS)
        await callback_query.message.delete()

        await state.clear()


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm_edit_choose_gender:'))
async def handle_face_swap_manage_edit_choose_gender_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    gender = callback_query.data.split(':')[1]

    face_swap_packages = await get_face_swap_packages_by_gender(gender)
    reply_markup = build_manage_face_swap_edit_choose_package_keyboard(user.language_code, face_swap_packages)
    await callback_query.message.edit_text(
        text=get_localization(user.language_code).FACE_SWAP_MANAGE_EDIT_CHOOSE_PACKAGE,
        reply_markup=reply_markup,
    )

    await state.update_data(gender=gender)


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm_edit_choose_package:'))
async def handle_face_swap_manage_edit_choose_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))
    user_data = await state.get_data()

    package_name = user_data.get('package_name', callback_query.data.split(':')[1])

    reply_markup = build_manage_face_swap_edit_keyboard(user.language_code)
    await callback_query.message.edit_text(
        text=get_localization(user.language_code).FACE_SWAP_MANAGE_EDIT,
        reply_markup=reply_markup,
    )

    await state.update_data(package_name=package_name)


async def show_picture(file: Dict, language_code: str, face_swap_package: FaceSwapPackage,
                       callback_query: CallbackQuery):
    try:
        file_name, file_status = file.get('name'), file.get('status')
        reply_markup = build_manage_face_swap_edit_picture_keyboard(language_code, file_name)

        photo_path = f'face_swap/{face_swap_package.gender.lower()}/{face_swap_package.name.lower()}/{file_name}'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_data = await photo.download()

        await callback_query.message.answer_photo(
            photo=BufferedInputFile(photo_data, filename=photo_path),
            caption=f'<b>{file_name}</b>\n\n{file_status}',
            reply_markup=reply_markup,
        )
    except Exception as e:
        await callback_query.message.answer(
            text=f'{file_name}\n\n{get_localization(language_code).ERROR}:\n{e}',
            parse_mode=None
        )


async def show_pictures(face_swap_package: FaceSwapPackage, language_code: str, callback_query: CallbackQuery):
    tasks = [
        show_picture(file,
                     language_code,
                     face_swap_package,
                     callback_query) for file in face_swap_package.files
    ]
    await asyncio.gather(*tasks)


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm_edit:'))
async def handle_face_swap_manage_edit_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'back':
        await handle_manage_face_swap(callback_query.message, str(callback_query.from_user.id))

        await callback_query.message.delete()

        await state.clear()
    else:
        user = await get_user(str(callback_query.from_user.id))
        user_data = await state.get_data()
        face_swap_package = await get_face_swap_package_by_name_and_gender(user_data['package_name'],
                                                                           user_data['gender'])
        await state.update_data(face_swap_package_id=face_swap_package.id)

        if action == 'change_status':
            reply_markup = build_manage_face_swap_edit_package_change_status_keyboard(user.language_code,
                                                                                      face_swap_package.status)
            await callback_query.message.edit_text(
                text=get_localization(user.language_code).FACE_SWAP_MANAGE_CHANGE_STATUS,
                reply_markup=reply_markup
            )
        elif action == 'show_pictures':
            await show_pictures(face_swap_package, user.language_code, callback_query)
        elif action == 'add_new_picture':
            reply_markup = build_manage_face_swap_add_picture_keyboard(user.language_code)
            await callback_query.message.edit_text(
                text=get_localization(user.language_code).FACE_SWAP_MANAGE_ADD_NEW_PICTURE,
                reply_markup=reply_markup,
            )
            await state.set_state(FaceSwap.waiting_for_face_swap_picture)


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm_edit_package_change_status:'))
async def handle_face_swap_manage_edit_package_change_status_selection(callback_query: CallbackQuery,
                                                                       state: FSMContext):
    await callback_query.answer()

    user_data = await state.get_data()

    status = callback_query.data.split(':')[1]

    if status == 'back':
        await handle_face_swap_manage_edit_choose_package_selection(callback_query, state)
        return

    keyboard = callback_query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data == status:
                if "✅" not in text:
                    text += " ✅"
                    keyboard_changed = True
            else:
                text = text.replace(" ✅", "")
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        await update_face_swap_package(user_data['face_swap_package_id'], {
            "status": status
        })
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm_edit_picture:'))
async def handle_face_swap_manage_edit_picture_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))
    user_data = await state.get_data()

    action, file_name = callback_query.data.split(':')[1], callback_query.data.split(':')[2]
    face_swap_package = await get_face_swap_package(user_data['face_swap_package_id'])
    file_status = FaceSwapPackageStatus.PRIVATE
    for file in face_swap_package.files:
        if file['name'] == file_name:
            file_status = file.get('status')
            break

    if action == 'change_status':
        reply_markup = build_manage_face_swap_edit_picture_change_status_keyboard(user.language_code, file_status)
        await callback_query.message.edit_caption(
            caption=get_localization(user.language_code).FACE_SWAP_MANAGE_CHANGE_STATUS,
            reply_markup=reply_markup,
        )
        await state.update_data(file_name=file_name)
    elif action == 'example_picture':
        await callback_query.message.bot.send_chat_action(chat_id=callback_query.message.chat.id,
                                                          action=constants.ChatAction.UPLOAD_PHOTO)

        user_photo = await firebase.bucket.get_blob(f'users/avatars/{user.id}.jpeg')
        user_photo_link = firebase.get_public_url(user_photo.name)

        image_path = f'face_swap/{face_swap_package.gender.lower()}/{face_swap_package.name.lower()}/{file_name}'
        image = await firebase.bucket.get_blob(image_path)
        image_link = firebase.get_public_url(image.name)

        face_swap_response = await get_face_swap_image(image_link, user_photo_link)

        await write_transaction(user_id=user.id,
                                type=TransactionType.EXPENSE,
                                service=ServiceType.FACE_SWAP,
                                amount=round(PRICE_FACE_SWAP * face_swap_response['seconds'], 6),
                                currency=Currency.USD,
                                quantity=1)

        await callback_query.message.reply_photo(
            photo=URLInputFile(face_swap_response['image'], filename=image_path),
            caption=file_name,
        )


@face_swap_router.callback_query(lambda c: c.data.startswith('fsm_edit_picture_change_status:'))
async def handle_face_swap_manage_edit_picture_change_status_selection(callback_query: CallbackQuery,
                                                                       state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))
    user_data = await state.get_data()

    status = callback_query.data.split(':')[1]
    if status == 'back':
        reply_markup = build_manage_face_swap_edit_picture_keyboard(user.language_code, user_data['file_name'])
        await callback_query.message.edit_reply_markup(reply_markup=reply_markup)
        return

    face_swap_package = await get_face_swap_package(user_data['face_swap_package_id'])
    for file in face_swap_package.files:
        if file['name'] == user_data['file_name']:
            file['status'] = status
            break

    keyboard = callback_query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data == status:
                if "✅" not in text:
                    text += " ✅"
                    keyboard_changed = True
            else:
                text = text.replace(" ✅", "")
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        await update_face_swap_package(user_data['face_swap_package_id'], {
            "files": face_swap_package.files
        })
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))
