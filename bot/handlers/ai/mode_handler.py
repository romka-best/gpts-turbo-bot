from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Model
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.ai.face_swap_handler import handle_face_swap
from bot.keyboards.common.common import build_recommendations_keyboard
from bot.keyboards.ai.mode import build_mode_keyboard
from bot.locales.main import get_localization, get_user_language

mode_router = Router()


@mode_router.message(Command("mode"))
async def mode(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_mode_keyboard(user_language_code, user.current_model)

    await message.answer(
        text=get_localization(user_language_code).MODE,
        reply_markup=reply_markup,
    )


@mode_router.callback_query(lambda c: c.data.startswith('mode:'))
async def handle_mode_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    chosen_model = callback_query.data.split(':')[1]

    keyboard = callback_query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data == chosen_model:
                if "✅" not in text:
                    text += " ✅"
                    keyboard_changed = True
            else:
                text = text.replace(" ✅", "")
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    user.current_model = chosen_model
    reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
    if keyboard_changed:
        await update_user(user_id, {
            "current_model": chosen_model,
        })
        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))

        await callback_query.message.reply(
            text=get_localization(user_language_code).switched(user.current_model),
            reply_markup=reply_markup,
        )
    else:
        await callback_query.message.reply(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )

    if chosen_model == Model.FACE_SWAP:
        await handle_face_swap(
            callback_query.bot,
            str(callback_query.message.chat.id),
            state,
            str(callback_query.from_user.id),
        )
