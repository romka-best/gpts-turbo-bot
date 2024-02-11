from typing import List

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    URLInputFile,
    InputMediaAudio,
)

from bot.database.main import firebase
from bot.database.models.common import Quota, DALLEResolution, DALLEQuality, Model
from bot.database.models.user import UserSettings
from bot.database.operations.chat import get_chat_by_user_id, update_chat, get_chats_by_user_id, delete_chat, reset_chat
from bot.database.operations.role import get_role_by_name, get_roles
from bot.database.operations.user import get_user, update_user
from bot.handlers.payment_handler import handle_buy
from bot.helpers.create_new_chat import create_new_chat
from bot.integrations.openAI import get_cost_for_image
from bot.keyboards.catalog import build_catalog_keyboard
from bot.keyboards.chats import (
    build_chats_keyboard,
    build_create_chat_keyboard,
    build_switch_chat_keyboard,
    build_reset_chat_keyboard,
    build_delete_chat_keyboard,
)
from bot.keyboards.common import build_recommendations_keyboard
from bot.keyboards.settings import (
    build_settings_choose_model_keyboard,
    build_settings_keyboard,
    build_voice_messages_settings_keyboard,
)
from bot.locales.main import get_localization
from bot.states.chats import Chats

settings_router = Router()


@settings_router.message(Command("settings"))
async def settings_choose_model(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user(str(message.from_user.id))

    reply_markup = build_settings_choose_model_keyboard(user.language_code)
    await message.answer(
        text=get_localization(user.language_code).SETTINGS_CHOOSE_MODEL,
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('settings_choose_model:'))
async def handle_settings_choose_model_selection(callback_query: CallbackQuery):
    user = await get_user(str(callback_query.from_user.id))

    dalle_cost = 1
    chosen_model = callback_query.data.split(':')[1]
    if chosen_model == Model.GPT3 or chosen_model == Model.GPT4:
        human_model = f"{get_localization(user.language_code).CHATGPT3} / {get_localization(user.language_code).CHATGPT4}"
    elif chosen_model == Model.DALLE3:
        dalle_cost = get_cost_for_image(
            user.settings[Model.DALLE3][UserSettings.QUALITY],
            user.settings[Model.DALLE3][UserSettings.RESOLUTION],
        )
        human_model = get_localization(user.language_code).DALLE3
    elif chosen_model == Model.FACE_SWAP:
        human_model = get_localization(user.language_code).FACE_SWAP
    elif chosen_model == Model.MUSIC_GEN:
        human_model = get_localization(user.language_code).MUSIC_GEN
    else:
        human_model = chosen_model

    reply_markup = build_settings_keyboard(user.language_code, chosen_model, user.settings)
    await callback_query.message.edit_text(
        text=get_localization(user.language_code).settings(human_model, chosen_model, dalle_cost),
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('setting:'))
async def handle_setting_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    chosen_setting = callback_query.data.split(':')[1]

    user = await get_user(str(callback_query.from_user.id))
    if chosen_setting == 'back':
        reply_markup = build_settings_choose_model_keyboard(user.language_code)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).SETTINGS_CHOOSE_MODEL,
            reply_markup=reply_markup,
        )
        return

    chosen_model = callback_query.data.split(':')[2]
    what_changed = None
    if chosen_setting == 'voice_messages':
        await handle_voice_messages(callback_query.message, user.id)
        return
    elif chosen_setting == 'manage_chats':
        await handle_chats(callback_query.message, user.id)
        return
    elif chosen_setting == 'manage_catalog':
        await handle_catalog(callback_query.message, user.id)
        return
    elif chosen_setting == DALLEResolution.LOW or chosen_setting == DALLEResolution.MEDIUM or chosen_setting == DALLEResolution.HIGH:
        user.settings[Model.DALLE3][UserSettings.RESOLUTION] = chosen_setting
        what_changed = UserSettings.RESOLUTION
    elif chosen_setting == DALLEQuality.STANDARD or chosen_setting == DALLEQuality.HD:
        user.settings[Model.DALLE3][UserSettings.QUALITY] = chosen_setting
        what_changed = UserSettings.QUALITY
    else:
        if chosen_model == Model.GPT3 or chosen_model == Model.GPT4:
            user.settings[Model.GPT3][chosen_setting] = not user.settings[Model.GPT3][chosen_setting]
            user.settings[Model.GPT4][chosen_setting] = not user.settings[Model.GPT4][chosen_setting]
        else:
            user.settings[chosen_model][chosen_setting] = not user.settings[chosen_model][chosen_setting]
        what_changed = chosen_setting

    keyboard = callback_query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":")[1]

            if what_changed == UserSettings.QUALITY:
                if callback_data == chosen_setting and "✅" not in text:
                    text += " ✅"
                    keyboard_changed = True
                elif callback_data == DALLEQuality.STANDARD or callback_data == DALLEQuality.HD:
                    text = text.replace(" ✅", "")
            elif what_changed == UserSettings.RESOLUTION:
                if callback_data == chosen_setting and "✅" not in text:
                    text += " ✅"
                    keyboard_changed = True
                elif callback_data == DALLEResolution.LOW or callback_data == DALLEResolution.MEDIUM or callback_data == DALLEResolution.HIGH:
                    text = text.replace(" ✅", "")
            elif (
                callback_data != DALLEQuality.STANDARD and callback_data != DALLEQuality.HD and
                callback_data != DALLEResolution.LOW and callback_data != DALLEResolution.MEDIUM and callback_data != DALLEResolution.HIGH
            ):
                if "✅" in text:
                    text = text.replace(" ✅", " ❌")
                    keyboard_changed = True
                else:
                    text = text.replace(" ❌", " ✅")
                    keyboard_changed = True
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        await update_user(
            user.id, {
                "settings": user.settings,
            },
        )

        dalle_cost = 1
        if chosen_model == Model.GPT3 or chosen_model == Model.GPT4:
            human_model = f"{get_localization(user.language_code).CHATGPT3} / {get_localization(user.language_code).CHATGPT4}"
        elif chosen_model == Model.DALLE3:
            dalle_cost = get_cost_for_image(
                user.settings[Model.DALLE3][UserSettings.QUALITY],
                user.settings[Model.DALLE3][UserSettings.RESOLUTION],
            )
            human_model = get_localization(user.language_code).DALLE3
        elif chosen_model == Model.FACE_SWAP:
            human_model = get_localization(user.language_code).FACE_SWAP
        elif chosen_model == Model.MUSIC_GEN:
            human_model = get_localization(user.language_code).MUSIC_GEN
        else:
            human_model = chosen_model
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).settings(human_model, chosen_model, dalle_cost),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard),
        )


async def handle_voice_messages(message: Message, user_id: str):
    user = await get_user(user_id)

    reply_markup = build_voice_messages_settings_keyboard(user.language_code, user.settings)
    await message.edit_text(
        text=get_localization(user.language_code).VOICE_MESSAGES,
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('voice_messages_setting:'))
async def handle_voice_messages_setting_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    chosen_setting = callback_query.data.split(':')[1]

    user = await get_user(str(callback_query.from_user.id))
    if chosen_setting == 'back':
        human_model = f"{get_localization(user.language_code).CHATGPT3} / {get_localization(user.language_code).CHATGPT4}"
        reply_markup = build_settings_keyboard(user.language_code, Model.GPT3, user.settings)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).settings(human_model, Model.GPT3),
            reply_markup=reply_markup,
        )
        return
    elif (
        chosen_setting == UserSettings.TURN_ON_VOICE_MESSAGES and not user.additional_usage_quota[Quota.VOICE_MESSAGES]
    ):
        user.settings[Model.GPT3][chosen_setting] = False
        user.settings[Model.GPT4][chosen_setting] = False
        await handle_buy(callback_query.message, str(callback_query.from_user.id))
        return
    elif chosen_setting == 'listen':
        voices: List[InputMediaAudio] = []
        voices_path = f'voices/{user.language_code}'
        for voice in ["alloy", "echo", "nova", "shimmer", "fable", "onyx"]:
            voice_filename = f"{voice}.mp3"
            voice = await firebase.bucket.get_blob(f"{voices_path}/{voice_filename}")
            voice_link = firebase.get_public_url(voice.name)
            voices.append(InputMediaAudio(media=voice_link, title=voice_filename))

        await callback_query.message.answer_media_group(
            media=voices,
        )
        return

    keyboard = callback_query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data == chosen_setting and chosen_setting == UserSettings.TURN_ON_VOICE_MESSAGES:
                if "✅" in text:
                    text = text.replace(" ✅", " ❌")
                    keyboard_changed = True
                else:
                    text = text.replace(" ❌", " ✅")
                    keyboard_changed = True
            elif callback_data == chosen_setting:
                if "✅" not in text:
                    text += " ✅"
                    keyboard_changed = True
            elif chosen_setting != UserSettings.TURN_ON_VOICE_MESSAGES:
                text = text.replace(" ✅", "")
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        if chosen_setting in ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]:
            user.settings[Model.GPT3][UserSettings.VOICE] = chosen_setting
            user.settings[Model.GPT4][UserSettings.VOICE] = chosen_setting
        else:
            user.settings[Model.GPT3][chosen_setting] = not user.settings[Model.GPT3][chosen_setting]
            user.settings[Model.GPT4][chosen_setting] = not user.settings[Model.GPT4][chosen_setting]

        await update_user(
            user.id, {
                "settings": user.settings,
            },
        )

        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))


async def handle_catalog(message: Message, user_id: str):
    user = await get_user(user_id)

    text = get_localization(user.language_code).CATALOG
    current_chat = await get_chat_by_user_id(user.id)
    roles = await get_roles()
    reply_markup = build_catalog_keyboard(user.language_code, current_chat.role, roles)

    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('catalog:'))
async def handle_catalog_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    role_name = callback_query.data.split(':')[1]
    if role_name == 'back':
        human_model = f"{get_localization(user.language_code).CHATGPT3} / {get_localization(user.language_code).CHATGPT4}"
        reply_markup = build_settings_keyboard(user.language_code, Model.GPT3, user.settings)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).settings(human_model, Model.GPT3),
            reply_markup=reply_markup,
        )
        return

    role_photo_path = f'roles/{role_name}.png'
    role_photo = await firebase.bucket.get_blob(role_photo_path)
    role_photo_link = firebase.get_public_url(role_photo.name)

    if not user.additional_usage_quota[Quota.ACCESS_TO_CATALOG]:
        text = get_localization(user.language_code).CATALOG_FORBIDDEN_ERROR
        await callback_query.message.reply_photo(
            photo=URLInputFile(role_photo_link, filename=role_photo_path),
            caption=text,
        )
    else:
        keyboard = callback_query.message.reply_markup.inline_keyboard
        keyboard_changed = False

        new_keyboard = []
        for row in keyboard:
            new_row = []
            for button in row:
                text = button.text
                callback_data = button.callback_data.split(":", 1)[1]

                if callback_data == role_name:
                    if "❌" in text:
                        text = text.replace(" ❌", " ✅")
                        keyboard_changed = True
                else:
                    text = text.replace(" ✅", " ❌")
                new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
            new_keyboard.append(new_row)

        if keyboard_changed:
            current_chat = await get_chat_by_user_id(user.id)
            await update_chat(current_chat.id, {
                "role": role_name,
            })

            await callback_query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard),
            )

            role = await get_role_by_name(role_name)
            await callback_query.message.reply_photo(
                photo=URLInputFile(role_photo_link, filename=role_photo_path),
                caption=role.translated_descriptions.get(user.language_code, 'en'),
            )


async def handle_chats(message: Message, user_id: str):
    user = await get_user(user_id)
    all_chats = await get_chats_by_user_id(user.id)
    current_chat = await get_chat_by_user_id(user.id)

    text = get_localization(user.language_code).chats(
        current_chat.title,
        len(all_chats),
        user.additional_usage_quota[Quota.ADDITIONAL_CHATS],
    )
    reply_markup = build_chats_keyboard(user.language_code)

    await message.edit_text(text=text, reply_markup=reply_markup)


@settings_router.callback_query(lambda c: c.data.startswith('chat:'))
async def handle_chat_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    action = callback_query.data.split(':')[1]

    if action == 'back':
        human_model = f"{get_localization(user.language_code).CHATGPT3} / {get_localization(user.language_code).CHATGPT4}"
        reply_markup = build_settings_keyboard(user.language_code, Model.GPT3, user.settings)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).settings(human_model, Model.GPT3),
            reply_markup=reply_markup,
        )
        return
    elif action == 'show':
        all_chats = await get_chats_by_user_id(user.id)
        text = ""
        for count, chat in enumerate(all_chats):
            text += f"\n{count + 1}. <b>{chat.title}</b>"

        await callback_query.message.answer(text=text)
    elif action == 'create':
        if user.additional_usage_quota[Quota.ADDITIONAL_CHATS] > 0:
            reply_markup = build_create_chat_keyboard(user.language_code)

            await callback_query.message.answer(text=get_localization(user.language_code).TYPE_CHAT_NAME,
                                                reply_markup=reply_markup)

            await state.set_state(Chats.waiting_for_chat_name)
        else:
            await callback_query.message.answer(text=get_localization(user.language_code).CREATE_CHAT_FORBIDDEN)
    elif action == 'switch':
        all_chats = await get_chats_by_user_id(user.id)

        if len(all_chats) > 1:
            current_chat = await get_chat_by_user_id(user.id)
            reply_markup = build_switch_chat_keyboard(user.language_code, current_chat.id, all_chats)

            await callback_query.message.answer(text=get_localization(user.language_code).SWITCH_CHAT,
                                                reply_markup=reply_markup)
        else:
            await callback_query.message.answer(text=get_localization(user.language_code).SWITCH_CHAT_FORBIDDEN)
    elif action == 'reset':
        reply_keyboard = build_reset_chat_keyboard(user.language_code)
        await callback_query.message.answer(
            text=get_localization(user.language_code).RESET_CHAT_WARNING,
            reply_markup=reply_keyboard,
        )
    elif action == 'delete':
        all_chats = await get_chats_by_user_id(user.id)

        if len(all_chats) > 1:
            current_chat = await get_chat_by_user_id(user.id)
            reply_markup = build_delete_chat_keyboard(user.language_code, current_chat.id, all_chats)

            await callback_query.message.answer(text=get_localization(user.language_code).DELETE_CHAT,
                                                reply_markup=reply_markup)
        else:
            await callback_query.message.answer(text=get_localization(user.language_code).DELETE_CHAT_FORBIDDEN)


@settings_router.callback_query(lambda c: c.data.startswith('switch_chat:'))
async def handle_switch_chat_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    chat_id = callback_query.data.split(':')[1]

    keyboard = callback_query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data == chat_id:
                if "❌" in text:
                    text = text.replace(" ❌", " ✅")
                    keyboard_changed = True
            else:
                text = text.replace(" ✅", " ❌")
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        await update_user(user.id, {
            "current_chat_id": chat_id
        })

        await callback_query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard)
        )

        reply_markup = await build_recommendations_keyboard(user)
        await callback_query.message.reply(
            text=get_localization(user.language_code).SWITCH_CHAT_SUCCESS,
            reply_markup=reply_markup,
        )


@settings_router.callback_query(lambda c: c.data.startswith('delete_chat:'))
async def handle_delete_chat_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    chat_id = callback_query.data.split(':')[1]

    keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data != chat_id:
                new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    await delete_chat(chat_id)

    await callback_query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard)
    )

    await callback_query.message.reply(text=get_localization(user.language_code).DELETE_CHAT_SUCCESS)


@settings_router.message(Chats.waiting_for_chat_name, ~F.text.startswith('/'))
async def chat_name_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    transaction = firebase.db.transaction()
    await create_new_chat(transaction, user, str(message.chat.id), message.text)

    await message.answer(get_localization(user.language_code).CREATE_CHAT_SUCCESS)

    await message.delete()

    await state.clear()


@settings_router.callback_query(lambda c: c.data.startswith('reset_chat:'))
async def handle_reset_chat_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    action = callback_query.data.split(':')[1]
    if action == 'approve':
        await reset_chat(user.current_chat_id)
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).RESET_CHAT_SUCCESS,
        )
