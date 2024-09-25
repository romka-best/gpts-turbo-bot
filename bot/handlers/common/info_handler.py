from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.models.common import Model
from bot.keyboards.common.info import (
    build_info_keyboard,
    build_info_text_models_keyboard,
    build_info_image_models_keyboard,
    build_info_music_models_keyboard,
    build_info_chosen_model_keyboard,
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
    if models_type == 'text':
        reply_keyboard = build_info_text_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_TEXT_MODELS,
            reply_markup=reply_keyboard,
        )
    elif models_type == 'image':
        reply_keyboard = build_info_image_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_IMAGE_MODELS,
            reply_markup=reply_keyboard,
        )
    elif models_type == 'music':
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
    reply_keyboard = build_info_chosen_model_keyboard(user_language_code, 'text')
    if model == Model.CHAT_GPT:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_CHATGPT,
            reply_markup=reply_keyboard,
        )
    elif model == Model.CLAUDE:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_CLAUDE,
            reply_markup=reply_keyboard,
        )
    elif model == Model.GEMINI:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_GEMINI,
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
    reply_keyboard = build_info_chosen_model_keyboard(user_language_code, 'image')
    if model == Model.DALL_E:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_DALL_E,
            reply_markup=reply_keyboard,
        )
    elif model == Model.MIDJOURNEY:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_MIDJOURNEY,
            reply_markup=reply_keyboard,
        )
    elif model == Model.STABLE_DIFFUSION:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_STABLE_DIFFUSION,
            reply_markup=reply_keyboard,
        )
    elif model == Model.FACE_SWAP:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_FACE_SWAP,
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
    reply_keyboard = build_info_chosen_model_keyboard(user_language_code, 'music')
    if model == Model.MUSIC_GEN:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_MUSIC_GEN,
            reply_markup=reply_keyboard,
        )
    elif model == Model.SUNO:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).INFO_SUNO,
            reply_markup=reply_keyboard,
        )
    else:
        text = get_localization(user_language_code).INFO
        reply_markup = build_info_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )


@info_router.callback_query(lambda c: c.data.startswith('info_chosen_model:'))
async def info_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    action, model_type = callback_query.data.split(':')[1], callback_query.data.split(':')[2]
    if action == 'back' and model_type == 'text':
        text = get_localization(user_language_code).INFO_TEXT_MODELS
        reply_markup = build_info_text_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )
    elif action == 'back' and model_type == 'image':
        text = get_localization(user_language_code).INFO_IMAGE_MODELS
        reply_markup = build_info_image_models_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )
    elif action == 'back' and model_type == 'music':
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
