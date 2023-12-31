from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Quota
from bot.database.operations.chat import get_chat_by_user_id, update_chat
from bot.database.operations.user import get_user
from bot.keyboards.catalog import build_catalog_keyboard
from bot.locales.main import get_localization

catalog_router = Router()


@catalog_router.message(Command("catalog"))
async def catalog(message: Message):
    user = await get_user(str(message.from_user.id))

    if not user.additional_usage_quota[Quota.ACCESS_TO_CATALOG]:
        text = get_localization(user.language_code).CATALOG_FORBIDDEN_ERROR
        await message.answer(text=text)
    else:
        text = get_localization(user.language_code).CATALOG
        current_chat = await get_chat_by_user_id(user.id)
        reply_markup = build_catalog_keyboard(user.language_code, current_chat.role)

        await message.answer(text=text,
                             reply_markup=reply_markup)


@catalog_router.callback_query(lambda c: c.data.startswith('catalog:'))
async def handle_catalog_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    role_name = callback_query.data.split(':')[1]

    user = await get_user(str(callback_query.from_user.id))

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

        await callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))

        text = getattr(get_localization(user.language_code), role_name)["description"]
        await callback_query.message.answer(text=text)
