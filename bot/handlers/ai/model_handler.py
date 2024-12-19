from typing import cast

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import config, MessageEffect
from bot.database.models.common import Model, ModelType
from bot.database.models.user import UserSettings
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.ai.eightify_handler import handle_eightify
from bot.handlers.ai.face_swap_handler import handle_face_swap
from bot.handlers.ai.music_gen_handler import handle_music_gen
from bot.handlers.ai.photoshop_ai_handler import handle_photoshop_ai
from bot.handlers.ai.suno_handler import handle_suno
from bot.handlers.common.catalog_handler import handle_catalog_prompts_model_type
from bot.handlers.common.info_handler import handle_info_selection
from bot.helpers.getters.get_human_model import get_human_model
from bot.helpers.getters.get_info_by_model import get_info_by_model
from bot.helpers.getters.get_model_type import get_model_type
from bot.helpers.getters.get_quota_by_model import get_quota_by_model
from bot.helpers.getters.get_switched_to_ai_model import get_switched_to_ai_model
from bot.integrations.openAI import get_cost_for_image
from bot.keyboards.ai.model import build_model_keyboard, build_switched_to_ai_keyboard
from bot.keyboards.settings.settings import build_settings_keyboard
from bot.locales.main import get_localization, get_user_language

model_router = Router()


@model_router.message(Command('model'))
async def model(message: Message, state: FSMContext):
    await state.clear()

    await handle_model(message, state, str(message.from_user.id), False, 0)


@model_router.message(Command('text'))
async def model_text(message: Message, state: FSMContext):
    await state.clear()

    await handle_model(message, state, str(message.from_user.id), False, 0)


@model_router.message(Command('summary'))
async def model_text(message: Message, state: FSMContext):
    await state.clear()

    await handle_model(message, state, str(message.from_user.id), False, 1)


@model_router.message(Command('image'))
async def model_image(message: Message, state: FSMContext):
    await state.clear()

    await handle_model(message, state, str(message.from_user.id), False, 2)


@model_router.message(Command('music'))
async def model_music(message: Message, state: FSMContext):
    await state.clear()

    await handle_model(message, state, str(message.from_user.id), False, 3)


@model_router.message(Command('video'))
async def model_video(message: Message, state: FSMContext):
    await state.clear()

    await handle_model(message, state, str(message.from_user.id), False, 4)


async def handle_model(message: Message, state: FSMContext, user_id: str, is_edit=False, page=0, chosen_model=None):
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_model_keyboard(
        user_language_code,
        user.current_model,
        user.settings[user.current_model][UserSettings.VERSION]
        if user.current_model == Model.CHAT_GPT or
           user.current_model == Model.CLAUDE or
           user.current_model == Model.GEMINI
        else '',
        page,
        chosen_model,
    )

    if is_edit:
        await message.edit_text(
            text=get_localization(user_language_code).MODEL,
            reply_markup=reply_markup,
        )
    else:
        await message.answer(
            text=get_localization(user_language_code).MODEL,
            reply_markup=reply_markup,
        )


@model_router.callback_query(lambda c: c.data.startswith('model:'))
async def handle_model_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    chosen_model = callback_query.data.split(':')[1]
    chosen_version = ''
    if chosen_model == 'page':
        return
    elif chosen_model == ModelType.TEXT or chosen_model == ModelType.IMAGE or chosen_model == ModelType.MUSIC:
        await handle_info_selection(callback_query, state, chosen_model)
        return
    elif chosen_model == 'next' or chosen_model == 'back':
        page = int(callback_query.data.split(':')[2])
        await handle_model(callback_query.message, state, str(callback_query.from_user.id), True, page)

        return
    elif chosen_model == Model.CHAT_GPT or chosen_model == Model.CLAUDE or chosen_model == Model.GEMINI:
        if len(callback_query.data.split(':')) > 2:
            action = callback_query.data.split(':')[2]
            if action == 'back':
                await handle_model(
                    callback_query.message,
                    state,
                    str(callback_query.from_user.id),
                    True,
                    0,
                    None,
                )
                return
            else:
                chosen_version = callback_query.data.split(':')[2]
        else:
            await handle_model(callback_query.message, state, str(callback_query.from_user.id), True, 0, chosen_model)
            return

    keyboard = callback_query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(':', 1)[1]

            if (
                (callback_data.startswith(chosen_model) and callback_data.endswith(chosen_version)) or
                callback_data == chosen_model
            ):
                if '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
            else:
                text = text.replace(' ✅', '')
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    user.current_model = chosen_model
    reply_markup = build_switched_to_ai_keyboard(user_language_code, user.current_model)
    if keyboard_changed:
        if chosen_model == Model.CHAT_GPT:
            user.settings[Model.CHAT_GPT][UserSettings.VERSION] = chosen_version
        elif chosen_model == Model.CLAUDE:
            user.settings[Model.CLAUDE][UserSettings.VERSION] = chosen_version
        elif chosen_model == Model.GEMINI:
            user.settings[Model.GEMINI][UserSettings.VERSION] = chosen_version

        await update_user(user_id, {
            'current_model': user.current_model,
            'settings': user.settings,
        })
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))

        text = await get_switched_to_ai_model(
            user,
            get_quota_by_model(user.current_model, user.settings[user.current_model][UserSettings.VERSION]),
            user_language_code,
        )
        await callback_query.message.reply(
            text=text,
            reply_markup=reply_markup,
            message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.FIRE),
            allow_sending_without_reply=True,
        )
    else:
        await callback_query.message.reply(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )

    if chosen_model == Model.EIGHTIFY:
        await handle_eightify(
            bot=callback_query.bot,
            chat_id=str(callback_query.message.chat.id),
            state=state,
            user_id=user_id,
        )
    elif chosen_model == Model.FACE_SWAP:
        await handle_face_swap(
            bot=callback_query.bot,
            chat_id=str(callback_query.message.chat.id),
            state=state,
            user_id=user_id,
        )
    elif chosen_model == Model.PHOTOSHOP_AI:
        await handle_photoshop_ai(
            bot=callback_query.bot,
            chat_id=str(callback_query.message.chat.id),
            state=state,
            user_id=user_id,
        )
    elif chosen_model == Model.MUSIC_GEN:
        await handle_music_gen(
            bot=callback_query.bot,
            chat_id=str(callback_query.message.chat.id),
            state=state,
            user_id=user_id,
        )
    elif chosen_model == Model.SUNO:
        await handle_suno(
            bot=callback_query.bot,
            chat_id=str(callback_query.message.chat.id),
            state=state,
            user_id=user_id,
        )


@model_router.callback_query(lambda c: c.data.startswith('switched_to_ai:'))
async def handle_switched_to_ai_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    action, model = callback_query.data.split(':')[1], cast(Model, callback_query.data.split(':')[2])
    if action == 'settings':
        user = await get_user(user_id)

        dall_e_cost = 1
        if model == Model.DALL_E:
            dall_e_cost = get_cost_for_image(
                user.settings[Model.DALL_E][UserSettings.QUALITY],
                user.settings[Model.DALL_E][UserSettings.RESOLUTION],
            )
        human_model = get_human_model(model, user_language_code)
        reply_markup = build_settings_keyboard(
            language_code=user_language_code,
            model=model,
            model_type=get_model_type(model),
            settings=user.settings,
        )
        await callback_query.message.answer(
            text=get_localization(user_language_code).settings(human_model, model, dall_e_cost),
            reply_markup=reply_markup,
        )
    elif action == 'info':
        info_text = get_info_by_model(model, user_language_code)
        await callback_query.message.answer(
            text=info_text,
        )
    elif action == 'examples':
        model_type = get_model_type(model)
        await state.update_data(prompt_model_type=model_type)
        await state.update_data(prompt_has_close_button=True)

        await handle_catalog_prompts_model_type(
            callback_query.message,
            user_id,
            state,
            False,
        )
