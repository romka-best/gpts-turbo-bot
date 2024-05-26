from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile

from bot.database.main import firebase
from bot.database.operations.role.getters import get_roles, get_role, get_role_by_name
from bot.database.operations.role.updaters import update_role
from bot.database.operations.role.writers import write_role
from bot.keyboards.admin.admin import build_admin_keyboard
from bot.locales.translate_text import translate_text
from bot.keyboards.admin.catalog import (
    build_manage_catalog_keyboard,
    build_manage_catalog_create_keyboard,
    build_manage_catalog_edit_keyboard,
)
from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_localization, localization_classes, get_user_language
from bot.states.catalog import Catalog

catalog_router = Router()


async def handle_manage_catalog(message: Message, user_id: str, state: FSMContext):
    user_language_code = await get_user_language(str(user_id), state.storage)

    roles = await get_roles()

    reply_markup = build_manage_catalog_keyboard(user_language_code, roles)
    await message.edit_text(
        text=get_localization(user_language_code).CATALOG_MANAGE,
        reply_markup=reply_markup,
    )


@catalog_router.callback_query(lambda c: c.data.startswith('catalog_manage:'))
async def handle_catalog_manage_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    if action == 'back':
        reply_markup = build_admin_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_INFO,
            reply_markup=reply_markup,
        )

        return
    elif action == 'create':
        reply_markup = build_manage_catalog_create_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).CATALOG_MANAGE_CREATE,
            reply_markup=reply_markup,
        )

        await state.set_state(Catalog.waiting_for_system_role_name)
    else:
        role = await get_role(action)
        role_photo_path = f'roles/{role.name}.png'
        role_photo = await firebase.bucket.get_blob(role_photo_path)
        role_photo_link = firebase.get_public_url(role_photo.name)

        reply_markup = build_manage_catalog_edit_keyboard(user_language_code, role.name)
        await callback_query.message.answer_photo(
            photo=URLInputFile(role_photo_link, filename=role_photo_path),
            caption=get_localization(user_language_code).catalog_manage_role_edit(
                role_system_name=role.name,
                role_names=role.translated_names,
                role_descriptions=role.translated_descriptions,
                role_instructions=role.translated_instructions,
            ),
            reply_markup=reply_markup,
        )

        await callback_query.message.delete()


@catalog_router.callback_query(lambda c: c.data.startswith('catalog_manage_create:'))
async def handle_catalog_manage_create_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'back':
        await handle_manage_catalog(callback_query.message, str(callback_query.from_user.id), state)

        await callback_query.message.delete()

        await state.clear()


@catalog_router.callback_query(lambda c: c.data.startswith('catalog_manage_create_role_confirmation:'))
async def handle_catalog_manage_create_role_confirmation_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'approve':
        user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)
        user_data = await state.get_data()

        await write_role(
            name=user_data['system_role_name'],
            translated_names=user_data['role_names'],
            translated_descriptions=user_data['role_descriptions'],
            translated_instructions=user_data['role_instructions'],
        )

        await callback_query.message.answer(text=get_localization(user_language_code).CATALOG_MANAGE_CREATE_SUCCESS)
        await callback_query.message.delete()

        await state.clear()


@catalog_router.message(Catalog.waiting_for_system_role_name, F.text, ~F.text.startswith('/'))
async def catalog_manage_create_role_system_name_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    system_role_name = message.text.upper()
    role = await get_role_by_name(system_role_name)
    if role:
        await message.answer(
            text=get_localization(user_language_code).CATALOG_MANAGE_CREATE_ALREADY_EXISTS_ERROR,
        )
    else:
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.answer(
            text=get_localization(user_language_code).CATALOG_MANAGE_CREATE_ROLE_NAME,
            reply_markup=reply_markup,
        )

        await state.update_data(system_role_name=system_role_name)
        await state.set_state(Catalog.waiting_for_role_name)


@catalog_router.message(Catalog.waiting_for_role_name, F.text, ~F.text.startswith('/'))
async def catalog_manage_create_role_name_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    role_names = {}
    for language_code in localization_classes.keys():
        if language_code == 'ru':
            role_names[language_code] = message.text
        else:
            translated_role_name = await translate_text(message.text, 'ru', language_code)
            if translated_role_name:
                role_names[language_code] = translated_role_name
            else:
                role_names[language_code] = message.text

    reply_markup = build_cancel_keyboard(user_language_code)
    await message.answer(
        text=get_localization(user_language_code).CATALOG_MANAGE_CREATE_ROLE_DESCRIPTION,
        reply_markup=reply_markup,
    )

    await state.update_data(role_names=role_names)
    await state.set_state(Catalog.waiting_for_role_description)


@catalog_router.message(Catalog.waiting_for_role_description, F.text, ~F.text.startswith('/'))
async def catalog_manage_create_role_description_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    role_descriptions = {}
    for language_code in localization_classes.keys():
        if language_code == 'ru':
            role_descriptions[language_code] = message.text
        else:
            translated_role_description = await translate_text(message.text, 'ru', language_code)
            if translated_role_description:
                role_descriptions[language_code] = translated_role_description
            else:
                role_descriptions[language_code] = message.text

    reply_markup = build_cancel_keyboard(user_language_code)
    await message.answer(
        text=get_localization(user_language_code).CATALOG_MANAGE_CREATE_ROLE_INSTRUCTION,
        reply_markup=reply_markup,
    )

    await state.update_data(role_descriptions=role_descriptions)
    await state.set_state(Catalog.waiting_for_role_instruction)


@catalog_router.message(Catalog.waiting_for_role_instruction, F.text, ~F.text.startswith('/'))
async def catalog_manage_create_role_instruction_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    role_instructions = {}
    for language_code in localization_classes.keys():
        if language_code == 'ru':
            role_instructions[language_code] = message.text
        else:
            translated_role_instruction = await translate_text(message.text, 'ru', language_code)
            if translated_role_instruction:
                role_instructions[language_code] = translated_role_instruction
            else:
                role_instructions[language_code] = message.text

    reply_markup = build_cancel_keyboard(user_language_code)
    await message.answer(
        text=get_localization(user_language_code).CATALOG_MANAGE_CREATE_ROLE_PHOTO,
        reply_markup=reply_markup,
    )

    await state.update_data(role_instructions=role_instructions)
    await state.set_state(Catalog.waiting_for_role_photo)


@catalog_router.callback_query(lambda c: c.data.startswith('catalog_manage_edit:'))
async def handle_catalog_manage_edit_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'back':
        await handle_manage_catalog(callback_query.message, str(callback_query.from_user.id), state)

        await callback_query.message.delete()

        await state.clear()
    else:
        action, system_role = callback_query.data.split(':')[1], callback_query.data.split(':')[2]

        user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

        reply_markup = build_cancel_keyboard(user_language_code)
        if action == 'name':
            await callback_query.message.edit_text(
                text=get_localization(user_language_code).CATALOG_MANAGE_EDIT_ROLE_NAME,
                reply_markup=reply_markup,
            )

            await state.set_state(Catalog.waiting_for_new_role_info)
        elif action == 'description':
            await callback_query.message.edit_text(
                text=get_localization(user_language_code).CATALOG_MANAGE_EDIT_ROLE_DESCRIPTION,
                reply_markup=reply_markup,
            )

            await state.set_state(Catalog.waiting_for_new_role_info)
        elif action == 'instruction':
            await callback_query.message.edit_text(
                text=get_localization(user_language_code).CATALOG_MANAGE_EDIT_ROLE_INSTRUCTION,
                reply_markup=reply_markup,
            )

            await state.set_state(Catalog.waiting_for_new_role_info)
        elif action == 'photo':
            await callback_query.message.edit_text(
                text=get_localization(user_language_code).CATALOG_MANAGE_EDIT_ROLE_PHOTO,
                reply_markup=reply_markup,
            )

            await state.set_state(Catalog.waiting_for_role_photo)

        await state.update_data(system_role=system_role, info_type=action)


@catalog_router.message(Catalog.waiting_for_new_role_info, F.text, ~F.text.startswith('/'))
async def catalog_manage_edit_role_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)
    user_data = await state.get_data()

    role_info = {}
    for language_code in localization_classes.keys():
        if language_code == 'ru':
            role_info[language_code] = message.text
        else:
            translated_role_name = await translate_text(message.text, 'ru', language_code)
            if translated_role_name:
                role_info[language_code] = translated_role_name
            else:
                role_info[language_code] = message.text

    role = await get_role_by_name(user_data['system_role'])
    info_type = user_data['info_type']
    if info_type == 'name':
        role.translated_names = role_info
    elif info_type == 'description':
        role.translated_descriptions = role_info
    elif info_type == 'instruction':
        role.translated_instructions = role_info
    await update_role(role.id, {
        'translated_names': role.translated_names,
        'translated_descriptions': role.translated_descriptions,
        'translated_instructions': role.translated_instructions,
    })

    await message.reply(text=get_localization(user_language_code).CATALOG_MANAGE_EDIT_SUCCESS)

    reply_markup = build_manage_catalog_edit_keyboard(user_language_code, role.name)
    await message.answer(
        text=get_localization(user_language_code).catalog_manage_role_edit(
            role_system_name=role.name,
            role_names=role.translated_names,
            role_descriptions=role.translated_descriptions,
            role_instructions=role.translated_instructions,
        ),
        reply_markup=reply_markup,
    )

    await state.clear()
