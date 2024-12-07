from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.config import config, MessageEffect
from bot.database.models.common import Model, PhotoshopAIAction
from bot.database.models.user import UserSettings
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.helpers.getters.get_quota_by_model import get_quota_by_model
from bot.helpers.getters.get_switched_to_ai_model import get_switched_to_ai_model
from bot.keyboards.ai.mode import build_switched_to_ai_keyboard
from bot.keyboards.ai.photoshop_ai import build_photoshop_ai_keyboard, build_photoshop_ai_chosen_keyboard
from bot.locales.main import get_user_language, get_localization
from bot.locales.types import LanguageCode
from bot.states.photoshop_ai import PhotoshopAI

photoshop_ai_router = Router()

PRICE_PHOTOSHOP_AI_RESTORATION = 0.000575
PRICE_PHOTOSHOP_AI_COLORIZATION = 0.000225
PRICE_PHOTOSHOP_AI_REMOVAL_BACKGROUND = 0.000575


@photoshop_ai_router.message(Command('photoshop'))
async def photoshop_ai(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.current_model == Model.PHOTOSHOP_AI:
        reply_markup = build_switched_to_ai_keyboard(user_language_code, Model.PHOTOSHOP_AI)
        await message.answer(
            text=get_localization(user_language_code).ALREADY_SWITCHED_TO_THIS_MODEL,
            reply_markup=reply_markup,
        )
    else:
        user.current_model = Model.PHOTOSHOP_AI
        await update_user(user_id, {
            'current_model': user.current_model,
        })

        text = await get_switched_to_ai_model(
            user,
            get_quota_by_model(user.current_model, user.settings[user.current_model][UserSettings.VERSION]),
            user_language_code,
        )
        reply_markup = build_switched_to_ai_keyboard(user_language_code, Model.PHOTOSHOP_AI)
        await message.answer(
            text=text,
            reply_markup=reply_markup,
            message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.FIRE),
        )

    await handle_photoshop_ai(message.bot, user.telegram_chat_id, state, user_id)


async def handle_photoshop_ai(bot: Bot, chat_id: str, state: FSMContext, user_id: str, chosen_action=None):
    user_language_code = await get_user_language(str(user_id), state.storage)

    if chosen_action:
        await handle_photoshop_ai_choose_selection(
            bot=bot,
            chat_id=chat_id,
            message_id=0,
            language_code=user_language_code,
            action_name=chosen_action,
            state=state,
        )
    else:
        reply_markup = build_photoshop_ai_keyboard(user_language_code)
        await bot.send_message(
            chat_id=chat_id,
            text=get_localization(user_language_code).PHOTOSHOP_AI_INFO,
            reply_markup=reply_markup,
        )


async def handle_photoshop_ai_choose_selection(
    bot: Bot,
    chat_id: str,
    message_id: int,
    language_code: LanguageCode,
    action_name: str,
    state: FSMContext,
):
    if (
        action_name == PhotoshopAIAction.RESTORATION or
        action_name == get_localization(language_code).PHOTOSHOP_AI_RESTORATION
    ):
        action_name = PhotoshopAIAction.RESTORATION
        text = get_localization(language_code).PHOTOSHOP_AI_RESTORATION_INFO
    elif (
        action_name == PhotoshopAIAction.COLORIZATION or
        action_name == get_localization(language_code).PHOTOSHOP_AI_COLORIZATION
    ):
        action_name = PhotoshopAIAction.COLORIZATION
        text = get_localization(language_code).PHOTOSHOP_AI_COLORIZATION_INFO
    elif (
        action_name == PhotoshopAIAction.REMOVAL_BACKGROUND or
        action_name == get_localization(language_code).PHOTOSHOP_AI_REMOVE_BACKGROUND
    ):
        action_name = PhotoshopAIAction.REMOVAL_BACKGROUND
        text = get_localization(language_code).PHOTOSHOP_AI_REMOVE_BACKGROUND_INFO
    else:
        return

    reply_markup = build_photoshop_ai_chosen_keyboard(language_code)
    if message_id != 0:
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        )
    else:
        await bot.send_message(
            text=text,
            chat_id=chat_id,
            reply_markup=reply_markup,
        )

    await state.update_data(photoshop_ai_action_name=action_name)
    await state.set_state(PhotoshopAI.waiting_for_photo)


@photoshop_ai_router.callback_query(lambda c: c.data.startswith('photoshop_ai:'))
async def photoshop_ai_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    action_name = callback_query.data.split(':')[1]
    await handle_photoshop_ai_choose_selection(
        bot=callback_query.message.bot,
        chat_id=str(callback_query.message.chat.id),
        message_id=callback_query.message.message_id,
        language_code=user_language_code,
        action_name=action_name,
        state=state,
    )


@photoshop_ai_router.callback_query(lambda c: c.data.startswith('photoshop_ai_chosen:'))
async def handle_photoshop_ai_action_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)
    reply_markup = build_photoshop_ai_keyboard(user_language_code)
    await callback_query.message.edit_text(
        text=get_localization(user_language_code).PHOTOSHOP_AI_INFO,
        reply_markup=reply_markup,
    )

    await state.clear()
