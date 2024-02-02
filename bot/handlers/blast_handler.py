import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database.operations.user import get_user
from bot.helpers.send_message_to_users import send_message_to_users
from bot.helpers.translate_text import translate_text
from bot.keyboards.blast import build_blast_keyboard, build_blast_confirmation_keyboard
from bot.keyboards.common import build_cancel_keyboard
from bot.locales.main import get_localization, localization_classes
from bot.states.blast import Blast
from bot.utils.is_admin import is_admin

blast_router = Router()


@blast_router.message(Command("blast"))
async def blast(message: Message, state: FSMContext):
    await state.clear()

    if is_admin(str(message.chat.id)):
        user = await get_user(str(message.from_user.id))

        reply_markup = build_blast_keyboard(user.language_code)
        await message.answer(
            text=get_localization(user.language_code).BLAST_CHOOSE_LANGUAGE,
            reply_markup=reply_markup,
        )


@blast_router.callback_query(lambda c: c.data.startswith('blast:'))
async def handle_blast_language_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    language = callback_query.data.split(':')[1]
    reply_markup = build_cancel_keyboard(user.language_code)
    if language == 'all':
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).BLAST_WRITE_IN_DEFAULT_LANGUAGE,
            reply_markup=reply_markup,
        )
    else:
        await callback_query.message.edit_text(
            text=get_localization(user.language_code).BLAST_WRITE_IN_CHOSEN_LANGUAGE,
            reply_markup=reply_markup,
        )

    await state.set_state(Blast.waiting_for_blast_letter)
    await state.update_data(blast_language=language)


@blast_router.message(Blast.waiting_for_blast_letter, ~F.text.startswith('/'))
async def blast_letter_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))
    user_data = await state.get_data()

    blast_letters = {}
    blast_language = user_data['blast_language']
    if blast_language != 'all':
        blast_letters[blast_language] = message.text
    else:
        for language_code in localization_classes.keys():
            if language_code == 'ru':
                blast_letters[language_code] = message.text
            else:
                translated_blast_letter = await translate_text(message.text, 'ru', language_code)
                if translated_blast_letter:
                    blast_letters[language_code] = translated_blast_letter
                else:
                    blast_letters[language_code] = message.text

    reply_markup = build_blast_confirmation_keyboard(user.language_code)
    await message.answer(
        text=get_localization(user.language_code).blast_confirmation(blast_letters),
        reply_markup=reply_markup,
    )

    await state.update_data(blast_letters=blast_letters)


@blast_router.callback_query(lambda c: c.data.startswith('blast_confirmation:'))
async def handle_blast_confirmation_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    if action == 'approve':
        user = await get_user(str(callback_query.from_user.id))
        user_data = await state.get_data()

        blast_language = user_data['blast_language']
        blast_letters = user_data['blast_letters']

        tasks = []
        if blast_language == 'all':
            for language_code in localization_classes.keys():
                tasks.append(
                    send_message_to_users(
                        bot=callback_query.bot,
                        language_code=language_code,
                        message=blast_letters[language_code],
                    )
                )
        else:
            tasks.append(
                send_message_to_users(
                    bot=callback_query.bot,
                    language_code=blast_language,
                    message=blast_letters[blast_language],
                )
            )
        await asyncio.gather(*tasks)

        await callback_query.message.answer(text=get_localization(user.language_code).BLAST_SUCCESS)
        await callback_query.message.delete()

        await state.clear()
