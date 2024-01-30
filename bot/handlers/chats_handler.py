from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.main import firebase
from bot.database.models.common import Quota
from bot.database.operations.chat import get_chats_by_user_id, get_chat_by_user_id, delete_chat
from bot.database.operations.user import get_user, update_user
from bot.helpers.create_new_chat import create_new_chat
from bot.keyboards.chats import (
    build_chats_keyboard,
    build_create_chat_keyboard,
    build_switch_chat_keyboard,
    build_delete_chat_keyboard,
)
from bot.keyboards.common import build_recommendations_keyboard
from bot.locales.main import get_localization
from bot.states.chats import Chats

chats_router = Router()


async def handle_chats(message: Message, user_id: str):
    user = await get_user(user_id)
    all_chats = await get_chats_by_user_id(user.id)
    current_chat = await get_chat_by_user_id(user.id)

    text = get_localization(user.language_code).chats(current_chat.title,
                                                      len(all_chats),
                                                      user.additional_usage_quota[Quota.ADDITIONAL_CHATS])
    reply_markup = build_chats_keyboard(user.language_code)

    await message.answer(text=text, reply_markup=reply_markup)


@chats_router.message(Command("chats"))
async def chats(message: Message, state: FSMContext):
    await state.clear()

    await handle_chats(message, str(message.from_user.id))


@chats_router.callback_query(lambda c: c.data.startswith('chat:'))
async def handle_chat_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    action = callback_query.data.split(':')[1]

    if action == 'show':
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
            await callback_query.message.delete()

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
            await callback_query.message.delete()
        else:
            await callback_query.message.answer(text=get_localization(user.language_code).SWITCH_CHAT_FORBIDDEN)
    elif action == 'delete':
        all_chats = await get_chats_by_user_id(user.id)

        if len(all_chats) > 1:
            current_chat = await get_chat_by_user_id(user.id)
            reply_markup = build_delete_chat_keyboard(user.language_code, current_chat.id, all_chats)

            await callback_query.message.answer(text=get_localization(user.language_code).DELETE_CHAT,
                                                reply_markup=reply_markup)
            await callback_query.message.delete()
        else:
            await callback_query.message.answer(text=get_localization(user.language_code).DELETE_CHAT_FORBIDDEN)


@chats_router.callback_query(Chats.waiting_for_chat_name, lambda c: c.data.startswith('create_chat:'))
async def handle_create_chat_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'back':
        await handle_chats(callback_query.message, str(callback_query.from_user.id))
        await callback_query.message.delete()

        await state.clear()


@chats_router.callback_query(lambda c: c.data.startswith('switch_chat:'))
async def handle_switch_chat_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    chat_id = callback_query.data.split(':')[1]

    if chat_id == 'back':
        await handle_chats(callback_query.message, str(callback_query.from_user.id))
        await callback_query.message.delete()
    else:
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


@chats_router.callback_query(lambda c: c.data.startswith('delete_chat:'))
async def handle_delete_chat_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    chat_id = callback_query.data.split(':')[1]

    if chat_id == 'back':
        await handle_chats(callback_query.message, str(callback_query.from_user.id))
        await callback_query.message.delete()
    else:
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


@chats_router.message(Chats.waiting_for_chat_name)
async def chat_name_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    transaction = firebase.db.transaction()
    await create_new_chat(transaction, user, str(message.chat.id), message.text)

    await message.answer(get_localization(user.language_code).CREATE_CHAT_SUCCESS)

    await message.delete()

    await state.clear()
