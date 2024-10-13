from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.models.common import ModelType
from bot.database.models.user import UserSettings
from bot.database.operations.user.getters import get_user
from bot.helpers.getters.get_info_by_model import get_info_by_model
from bot.helpers.getters.get_switched_to_ai_model import get_switched_to_ai_model
from bot.keyboards.ai.mode import build_switched_to_ai_keyboard
from bot.keyboards.common.info import (
    build_info_keyboard,
    build_info_text_models_keyboard,
    build_info_image_models_keyboard,
    build_info_music_models_keyboard,
    build_info_chosen_model_type_keyboard,
)
from bot.locales.main import get_user_language, get_localization

info_router = Router()


@info_router.message(Command('info'))
async def info(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    text = get_localization(user_language_code).INFO
    reply_markup = build_info_keyboard(user_language_code)
    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


@info_router.callback_query(lambda c: c.data.startswith('info:'))
async def info_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    models_type = callback_query.data.split(':')[1]
    if models_type == ModelType.TEXT:
        reply_keyboard = build_info_text_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_TEXT_MODELS,
            reply_markup=reply_keyboard,
        )
    elif models_type == ModelType.IMAGE:
        reply_keyboard = build_info_image_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_IMAGE_MODELS,
            reply_markup=reply_keyboard,
        )
    elif models_type == ModelType.MUSIC:
        reply_keyboard = build_info_music_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_MUSIC_MODELS,
            reply_markup=reply_keyboard,
        )
    else:
        await callback_query.message.delete()


@info_router.callback_query(lambda c: c.data.startswith('info_text_models:'))
async def info_text_models_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    model = callback_query.data.split(':')[1]
    info_text = get_info_by_model(model, user_language_code)
    reply_keyboard = build_info_chosen_model_type_keyboard(user_language_code, ModelType.TEXT)
    if info_text:
        await callback_query.message.edit_text(
            text=info_text,
            reply_markup=reply_keyboard,
        )
    else:
        text = get_localization(user_language_code).INFO
        reply_markup = build_info_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )


@info_router.callback_query(lambda c: c.data.startswith('info_image_models:'))
async def info_image_models_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    model = callback_query.data.split(':')[1]
    info_text = get_info_by_model(model, user_language_code)
    reply_keyboard = build_info_chosen_model_type_keyboard(user_language_code, ModelType.IMAGE)
    if info_text:
        await callback_query.message.edit_text(
            text=info_text,
            reply_markup=reply_keyboard,
        )
    else:
        text = get_localization(user_language_code).INFO
        reply_markup = build_info_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )


@info_router.callback_query(lambda c: c.data.startswith('info_music_models:'))
async def info_music_models_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    model = callback_query.data.split(':')[1]
    info_text = get_info_by_model(model, user_language_code)
    reply_keyboard = build_info_chosen_model_type_keyboard(user_language_code, ModelType.MUSIC)
    if info_text:
        await callback_query.message.edit_text(
            text=info_text,
            reply_markup=reply_keyboard,
        )
    else:
        text = get_localization(user_language_code).INFO
        reply_markup = build_info_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )


@info_router.callback_query(lambda c: c.data.startswith('info_chosen_model_type:'))
async def info_model_type_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    action, model_type = callback_query.data.split(':')[1], callback_query.data.split(':')[2]
    if action == 'back' and model_type == ModelType.TEXT:
        text = get_localization(user_language_code).INFO_TEXT_MODELS
        reply_markup = build_info_text_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )
    elif action == 'back' and model_type == ModelType.IMAGE:
        text = get_localization(user_language_code).INFO_IMAGE_MODELS
        reply_markup = build_info_image_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )
    elif action == 'back' and model_type == ModelType.MUSIC:
        text = get_localization(user_language_code).INFO_MUSIC_MODELS
        reply_markup = build_info_music_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )
    else:
        text = get_localization(user_language_code).INFO
        reply_markup = build_info_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )
