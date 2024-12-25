from typing import Optional, cast

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
)

from bot.database.main import firebase
from bot.database.models.common import (
    Model,
    ModelType,
    Quota,
    SendType,
    AspectRatio,
    VideoSummaryFocus,
    VideoSummaryFormat,
    VideoSummaryAmount,
    DALLEResolution,
    DALLEQuality,
    MidjourneyVersion,
    FluxSafetyTolerance,
    SunoVersion,
    RunwayResolution,
    RunwayDuration, KlingDuration, KlingMode,
)
from bot.database.models.user import UserSettings, UserGender
from bot.database.operations.chat.deleters import delete_chat, reset_chat
from bot.database.operations.chat.getters import get_chat_by_user_id, get_chats_by_user_id
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.common.catalog_handler import handle_catalog_digital_employees
from bot.handlers.payment.payment_handler import handle_buy
from bot.helpers.creaters.create_new_chat import create_new_chat
from bot.helpers.getters.get_human_model import get_human_model
from bot.helpers.getters.get_model_type import get_model_type
from bot.integrations.kling import Kling
from bot.integrations.openAI import get_cost_for_image
from bot.integrations.runway import get_cost_for_video
from bot.keyboards.common.common import build_buy_motivation_keyboard
from bot.keyboards.settings.chats import (
    build_chats_keyboard,
    build_create_chat_keyboard,
    build_switch_chat_keyboard,
    build_reset_chat_keyboard,
    build_delete_chat_keyboard,
)
from bot.keyboards.settings.settings import (
    build_settings_keyboard,
    build_settings_choose_model_type_keyboard,
    build_settings_choose_text_model_keyboard,
    build_settings_choose_summary_model_keyboard,
    build_settings_choose_image_model_keyboard,
    build_settings_choose_music_model_keyboard,
    build_settings_choose_video_model_keyboard,
    build_voice_messages_settings_keyboard,
)
from bot.locales.main import get_localization, get_user_language
from bot.states.common.chats import Chats

settings_router = Router()


@settings_router.message(Command('settings'))
async def settings_choose_model(message: Message, state: FSMContext):
    await state.clear()

    await handle_settings(message, str(message.from_user.id), state, True)


async def handle_settings(message: Message, user_id: str, state: FSMContext, advanced_mode=False):
    user_language_code = await get_user_language(user_id, state.storage)

    if advanced_mode:
        user = await get_user(user_id)

        generation_cost = 1
        if user.current_model == Model.DALL_E:
            generation_cost = get_cost_for_image(
                user.settings[Model.DALL_E][UserSettings.QUALITY],
                user.settings[Model.DALL_E][UserSettings.RESOLUTION],
            )
        elif user.current_model == Model.KLING:
            generation_cost = Kling.get_cost_for_video(
                user.settings[Model.KLING][UserSettings.MODE],
                user.settings[Model.KLING][UserSettings.DURATION],
            )
        elif user.current_model == Model.RUNWAY:
            generation_cost = get_cost_for_video(
                user.settings[Model.RUNWAY][UserSettings.DURATION],
            )
        human_model = get_human_model(user.current_model, user_language_code)
        reply_markup = build_settings_keyboard(
            language_code=user_language_code,
            model=user.current_model,
            model_type=get_model_type(user.current_model),
            settings=user.settings,
        )
        await message.answer(
            text=get_localization(user_language_code).settings(human_model, user.current_model, generation_cost),
            reply_markup=reply_markup,
        )
    else:
        reply_markup = build_settings_choose_model_type_keyboard(user_language_code)
        await message.answer(
            text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL_TYPE,
            reply_markup=reply_markup,
        )


@settings_router.callback_query(lambda c: c.data.startswith('settings_choose_model_type:'))
async def handle_settings_choose_model_type_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    chosen_model_type = callback_query.data.split(':')[1]
    if chosen_model_type == 'text_models':
        reply_markup = build_settings_choose_text_model_keyboard(user_language_code)
    elif chosen_model_type == 'summary_models':
        reply_markup = build_settings_choose_summary_model_keyboard(user_language_code)
    elif chosen_model_type == 'image_models':
        reply_markup = build_settings_choose_image_model_keyboard(user_language_code)
    elif chosen_model_type == 'music_models':
        reply_markup = build_settings_choose_music_model_keyboard(user_language_code)
    elif chosen_model_type == 'video_models':
        reply_markup = build_settings_choose_video_model_keyboard(user_language_code)
    else:
        return

    await callback_query.message.edit_text(
        text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL,
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('settings_choose_text_model:'))
async def handle_settings_choose_text_model_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    chosen_model = cast(Model, callback_query.data.split(':')[1])
    if chosen_model == 'back':
        reply_markup = build_settings_choose_model_type_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL_TYPE,
            reply_markup=reply_markup,
        )
        return

    human_model = get_human_model(chosen_model, user_language_code)
    reply_markup = build_settings_keyboard(user_language_code, chosen_model, ModelType.TEXT, user.settings)
    await callback_query.message.edit_text(
        text=get_localization(user_language_code).settings(human_model, chosen_model),
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('settings_choose_summary_model:'))
async def handle_settings_choose_summary_model_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    chosen_model = cast(Model, callback_query.data.split(':')[1])
    if chosen_model == 'back':
        reply_markup = build_settings_choose_model_type_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL_TYPE,
            reply_markup=reply_markup,
        )
        return

    human_model = get_human_model(chosen_model, user_language_code)
    reply_markup = build_settings_keyboard(user_language_code, chosen_model, ModelType.SUMMARY, user.settings)
    await callback_query.message.edit_text(
        text=get_localization(user_language_code).settings(human_model, chosen_model),
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('settings_choose_image_model:'))
async def handle_settings_choose_image_model_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    generation_cost = 1
    chosen_model = cast(Model, callback_query.data.split(':')[1])
    if chosen_model == 'back':
        reply_markup = build_settings_choose_model_type_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL_TYPE,
            reply_markup=reply_markup,
        )
        return
    elif chosen_model == Model.DALL_E:
        generation_cost = get_cost_for_image(
            user.settings[Model.DALL_E][UserSettings.QUALITY],
            user.settings[Model.DALL_E][UserSettings.RESOLUTION],
        )

    human_model = get_human_model(chosen_model, user_language_code)
    reply_markup = build_settings_keyboard(user_language_code, chosen_model, ModelType.IMAGE, user.settings)
    await callback_query.message.edit_text(
        text=get_localization(user_language_code).settings(human_model, chosen_model, generation_cost),
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('settings_choose_music_model:'))
async def handle_settings_choose_music_model_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    chosen_model = cast(Model, callback_query.data.split(':')[1])
    if chosen_model == 'back':
        reply_markup = build_settings_choose_model_type_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL_TYPE,
            reply_markup=reply_markup,
        )
        return

    human_model = get_human_model(chosen_model, user_language_code)
    reply_markup = build_settings_keyboard(user_language_code, chosen_model, ModelType.MUSIC, user.settings)
    await callback_query.message.edit_text(
        text=get_localization(user_language_code).settings(human_model, chosen_model),
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('settings_choose_video_model:'))
async def handle_settings_choose_video_model_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    generation_cost = 1
    chosen_model = cast(Model, callback_query.data.split(':')[1])
    if chosen_model == 'back':
        reply_markup = build_settings_choose_model_type_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL_TYPE,
            reply_markup=reply_markup,
        )
        return
    elif chosen_model == Model.KLING:
        generation_cost = Kling.get_cost_for_video(
            user.settings[Model.KLING][UserSettings.MODE],
            user.settings[Model.KLING][UserSettings.DURATION],
        )
    elif chosen_model == Model.RUNWAY:
        generation_cost = get_cost_for_video(
            user.settings[Model.RUNWAY][UserSettings.DURATION],
        )

    human_model = get_human_model(chosen_model, user_language_code)
    reply_markup = build_settings_keyboard(user_language_code, chosen_model, ModelType.VIDEO, user.settings)
    await callback_query.message.edit_text(
        text=get_localization(user_language_code).settings(human_model, chosen_model, generation_cost),
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('setting:'))
async def handle_setting_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    chosen_setting = callback_query.data.split(':')[1]

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if chosen_setting == 'back':
        model_type = callback_query.data.split(':')[2]
        if model_type == ModelType.TEXT:
            reply_markup = build_settings_choose_text_model_keyboard(user_language_code)
        elif model_type == ModelType.SUMMARY:
            reply_markup = build_settings_choose_summary_model_keyboard(user_language_code)
        elif model_type == ModelType.IMAGE:
            reply_markup = build_settings_choose_image_model_keyboard(user_language_code)
        elif model_type == ModelType.MUSIC:
            reply_markup = build_settings_choose_music_model_keyboard(user_language_code)
        elif model_type == ModelType.VIDEO:
            reply_markup = build_settings_choose_video_model_keyboard(user_language_code)
        else:
            return

        await callback_query.message.edit_text(
            text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL,
            reply_markup=reply_markup,
        )
        return
    elif chosen_setting == 'nothing':
        return

    chosen_model = cast(Model, callback_query.data.split(':')[2])

    if chosen_setting == 'voice_messages':
        await handle_voice_messages(callback_query.message, user_id, state, chosen_model)
        return
    elif chosen_setting == 'manage_chats':
        await handle_chats(callback_query.message, user_id, state, chosen_model)
        return
    elif chosen_setting == 'manage_catalog':
        await handle_catalog_digital_employees(callback_query.message, user_id, state, chosen_model, True)
        return

    if (
        chosen_setting == VideoSummaryFocus.INSIGHTFUL or
        chosen_setting == VideoSummaryFocus.FUNNY or
        chosen_setting == VideoSummaryFocus.ACTIONABLE or
        chosen_setting == VideoSummaryFocus.CONTROVERSIAL
    ):
        user.settings[chosen_model][UserSettings.FOCUS] = chosen_setting
        what_changed = UserSettings.FOCUS
    elif chosen_setting == VideoSummaryFormat.LIST or chosen_setting == VideoSummaryFormat.FAQ:
        user.settings[chosen_model][UserSettings.FORMAT] = chosen_setting
        what_changed = UserSettings.FORMAT
    elif chosen_setting == VideoSummaryAmount.SHORT or chosen_setting == VideoSummaryAmount.AUTO or chosen_setting == VideoSummaryAmount.DETAILED:
        user.settings[chosen_model][UserSettings.AMOUNT] = chosen_setting
        what_changed = UserSettings.AMOUNT
    elif chosen_setting == DALLEResolution.LOW or chosen_setting == DALLEResolution.MEDIUM or chosen_setting == DALLEResolution.HIGH:
        user.settings[Model.DALL_E][UserSettings.RESOLUTION] = chosen_setting
        if chosen_setting == DALLEResolution.LOW:
            user.settings[Model.DALL_E][UserSettings.ASPECT_RATIO] = AspectRatio.SQUARE
        elif chosen_setting == DALLEResolution.MEDIUM:
            user.settings[Model.DALL_E][UserSettings.ASPECT_RATIO] = AspectRatio.PORTRAIT
        elif chosen_setting == DALLEResolution.HIGH:
            user.settings[Model.DALL_E][UserSettings.ASPECT_RATIO] = AspectRatio.LANDSCAPE
        what_changed = UserSettings.RESOLUTION
    elif chosen_setting == DALLEQuality.STANDARD or chosen_setting == DALLEQuality.HD:
        user.settings[Model.DALL_E][UserSettings.QUALITY] = chosen_setting
        what_changed = UserSettings.QUALITY
    elif chosen_setting == MidjourneyVersion.V5 or chosen_setting == MidjourneyVersion.V6:
        user.settings[Model.MIDJOURNEY][UserSettings.VERSION] = chosen_setting
        what_changed = UserSettings.VERSION
    elif (
        chosen_setting == str(FluxSafetyTolerance.STRICT) or
        chosen_setting == str(FluxSafetyTolerance.MIDDLE) or
        chosen_setting == str(FluxSafetyTolerance.PERMISSIVE)
    ):
        user.settings[Model.FLUX][UserSettings.SAFETY_TOLERANCE] = int(chosen_setting)
        what_changed = UserSettings.SAFETY_TOLERANCE
    elif chosen_setting == UserGender.MALE or chosen_setting == UserGender.FEMALE:
        user.settings[Model.FACE_SWAP][UserSettings.GENDER] = chosen_setting
        what_changed = UserSettings.GENDER
    elif (
        chosen_setting == str(RunwayDuration.SECONDS_5) or
        chosen_setting == str(RunwayDuration.SECONDS_10) or
        chosen_setting == str(KlingDuration.SECONDS_5) or
        chosen_setting == str(KlingDuration.SECONDS_10)
    ):
        user.settings[chosen_model][UserSettings.DURATION] = int(chosen_setting)
        what_changed = UserSettings.DURATION
    elif (
        chosen_setting == 'SQUARE' or
        chosen_setting == 'LANDSCAPE' or
        chosen_setting == 'PORTRAIT' or
        chosen_setting == 'CINEMASCOPE_HORIZONTAL' or
        chosen_setting == 'CINEMASCOPE_VERTICAL' or
        chosen_setting == 'STANDARD_HORIZONTAL' or
        chosen_setting == 'STANDARD_VERTICAL' or
        chosen_setting == 'BANNER_HORIZONTAL' or
        chosen_setting == 'BANNER_VERTICAL' or
        chosen_setting == 'CLASSIC_HORIZONTAL' or
        chosen_setting == 'CLASSIC_VERTICAL'
    ):
        user.settings[chosen_model][UserSettings.ASPECT_RATIO] = getattr(
            AspectRatio,
            chosen_setting,
            AspectRatio.SQUARE,
        )
        if chosen_model == Model.RUNWAY:
            if user.settings[chosen_model][UserSettings.ASPECT_RATIO] == AspectRatio.PORTRAIT:
                user.settings[chosen_model][UserSettings.RESOLUTION] = RunwayResolution.PORTRAIT
            else:
                user.settings[chosen_model][UserSettings.RESOLUTION] = RunwayResolution.LANDSCAPE
        what_changed = UserSettings.ASPECT_RATIO
    elif (
        chosen_setting == SendType.TEXT or
        chosen_setting == SendType.IMAGE or
        chosen_setting == SendType.DOCUMENT or
        chosen_setting == SendType.AUDIO or
        chosen_setting == SendType.VIDEO
    ):
        user.settings[chosen_model][UserSettings.SEND_TYPE] = chosen_setting
        what_changed = UserSettings.SEND_TYPE
    elif chosen_setting == SunoVersion.V3 or chosen_setting == SunoVersion.V3_5 or chosen_setting == SunoVersion.V4:
        user.settings[Model.SUNO][UserSettings.VERSION] = chosen_setting
        what_changed = UserSettings.VERSION
    elif chosen_setting == KlingMode.STANDARD or chosen_setting == KlingMode.PRO:
        user.settings[Model.KLING][UserSettings.MODE] = chosen_setting
        what_changed = UserSettings.MODE
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
            callback_data = button.callback_data.split(':')[1]

            if what_changed == UserSettings.VERSION:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == MidjourneyVersion.V5 or callback_data == MidjourneyVersion.V6
                ) or (
                    callback_data == SunoVersion.V3 or callback_data == SunoVersion.V3_5 or callback_data == SunoVersion.V4
                ):
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.FOCUS:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == VideoSummaryFocus.INSIGHTFUL or
                    callback_data == VideoSummaryFocus.FUNNY or
                    callback_data == VideoSummaryFocus.ACTIONABLE or
                    callback_data == VideoSummaryFocus.CONTROVERSIAL
                ):
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.FORMAT:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == VideoSummaryFormat.LIST or
                    callback_data == VideoSummaryFormat.FAQ
                ):
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.AMOUNT:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == VideoSummaryAmount.SHORT or
                    callback_data == VideoSummaryAmount.AUTO or
                    callback_data == VideoSummaryAmount.DETAILED
                ):
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.QUALITY:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif callback_data == DALLEQuality.STANDARD or callback_data == DALLEQuality.HD:
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.RESOLUTION:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif callback_data == DALLEResolution.LOW or callback_data == DALLEResolution.MEDIUM or callback_data == DALLEResolution.HIGH:
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.ASPECT_RATIO:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == 'SQUARE' or
                    callback_data == 'LANDSCAPE' or
                    callback_data == 'PORTRAIT' or
                    callback_data == 'CINEMASCOPE_HORIZONTAL' or
                    callback_data == 'CINEMASCOPE_VERTICAL' or
                    callback_data == 'STANDARD_HORIZONTAL' or
                    callback_data == 'STANDARD_VERTICAL' or
                    callback_data == 'BANNER_HORIZONTAL' or
                    callback_data == 'BANNER_VERTICAL' or
                    callback_data == 'CLASSIC_HORIZONTAL' or
                    callback_data == 'CLASSIC_VERTICAL'
                ):
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.SEND_TYPE:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == SendType.TEXT or
                    callback_data == SendType.IMAGE or
                    callback_data == SendType.DOCUMENT or
                    callback_data == SendType.AUDIO or
                    callback_data == SendType.VIDEO
                ):
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.SAFETY_TOLERANCE:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == str(FluxSafetyTolerance.STRICT) or
                    callback_data == str(FluxSafetyTolerance.MIDDLE) or
                    callback_data == str(FluxSafetyTolerance.PERMISSIVE)
                ):
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.GENDER:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif callback_data == UserGender.MALE or callback_data == UserGender.FEMALE:
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.DURATION:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == str(RunwayDuration.SECONDS_5) or
                    callback_data == str(RunwayDuration.SECONDS_10) or
                    callback_data == str(KlingDuration.SECONDS_5) or
                    callback_data == str(KlingDuration.SECONDS_10)
                ):
                    text = text.replace(' ✅', '')
            elif what_changed == UserSettings.MODE:
                if callback_data == chosen_setting and '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
                elif (
                    callback_data == KlingMode.STANDARD or
                    callback_data == KlingMode.PRO
                ):
                    text = text.replace(' ✅', '')
            elif (
                chosen_setting == callback_data and
                callback_data != DALLEQuality.STANDARD and callback_data != DALLEQuality.HD and
                callback_data != DALLEResolution.LOW and callback_data != DALLEResolution.MEDIUM and callback_data != DALLEResolution.HIGH
            ):
                if '✅' in text:
                    text = text.replace(' ✅', ' ❌')
                    keyboard_changed = True
                else:
                    text = text.replace(' ❌', ' ✅')
                    keyboard_changed = True
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        await update_user(
            user_id, {
                'settings': user.settings,
            },
        )

        generation_cost = 1
        if chosen_model == Model.DALL_E:
            generation_cost = get_cost_for_image(
                user.settings[Model.DALL_E][UserSettings.QUALITY],
                user.settings[Model.DALL_E][UserSettings.RESOLUTION],
            )
        elif chosen_model == Model.KLING:
            generation_cost = Kling.get_cost_for_video(
                user.settings[Model.KLING][UserSettings.MODE],
                user.settings[Model.KLING][UserSettings.DURATION],
            )
        elif chosen_model == Model.RUNWAY:
            generation_cost = get_cost_for_video(
                user.settings[Model.RUNWAY][UserSettings.DURATION],
            )
        human_model = get_human_model(chosen_model, user_language_code)

        await callback_query.message.edit_text(
            text=get_localization(user_language_code).settings(human_model, chosen_model, generation_cost),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard),
        )


async def handle_voice_messages(message: Message, user_id: str, state: FSMContext, model: Optional[Model] = None):
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_voice_messages_settings_keyboard(user_language_code, user.settings, model)
    await message.edit_text(
        text=get_localization(user_language_code).SETTINGS_VOICE_MESSAGES,
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('voice_messages_setting:'))
async def handle_voice_messages_setting_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    chosen_setting = callback_query.data.split(':')[1]

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if chosen_setting == 'back':
        if len(callback_query.data.split(':')) == 3:
            chosen_model = cast(Model, callback_query.data.split(':')[2])
            human_model = get_human_model(chosen_model, user_language_code)
            reply_markup = build_settings_keyboard(
                language_code=user_language_code,
                model=chosen_model,
                model_type=get_model_type(chosen_model),
                settings=user.settings,
            )
            await callback_query.message.edit_text(
                text=get_localization(user_language_code).settings(human_model, chosen_model),
                reply_markup=reply_markup,
            )
        else:
            reply_markup = build_settings_choose_text_model_keyboard(user_language_code)
            await callback_query.message.edit_text(
                text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL,
                reply_markup=reply_markup,
            )

        return
    elif (
        chosen_setting == UserSettings.TURN_ON_VOICE_MESSAGES and
        not user.daily_limits[Quota.VOICE_MESSAGES] and
        not user.additional_usage_quota[Quota.VOICE_MESSAGES]
    ):
        user.settings[Model.CHAT_GPT][chosen_setting] = False
        user.settings[Model.CLAUDE][chosen_setting] = False
        user.settings[Model.GEMINI][chosen_setting] = False
        user.settings[Model.GROK][chosen_setting] = False
        user.settings[Model.PERPLEXITY][chosen_setting] = False

        user.settings[Model.EIGHTIFY][chosen_setting] = False
        user.settings[Model.GEMINI_VIDEO][chosen_setting] = False
        await handle_buy(callback_query.message, user_id, state)

        return
    elif chosen_setting == 'listen':
        voices: list[InputMediaAudio] = []
        voices_path = f'voices/{user_language_code}'
        for voice_name in ['alloy', 'echo', 'nova', 'shimmer', 'fable', 'onyx']:
            voice_filename = f'{voice_name}.mp3'
            voice = await firebase.bucket.get_blob(f'{voices_path}/{voice_filename}')
            voice_link = firebase.get_public_url(voice.name)
            voices.append(InputMediaAudio(media=voice_link, title=voice_name))

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
            callback_data = button.callback_data.split(':', 1)[1]

            if callback_data == chosen_setting and chosen_setting == UserSettings.TURN_ON_VOICE_MESSAGES:
                if '✅' in text:
                    text = text.replace(' ✅', ' ❌')
                    keyboard_changed = True
                else:
                    text = text.replace(' ❌', ' ✅')
                    keyboard_changed = True
            elif callback_data == chosen_setting:
                if '✅' not in text:
                    text += ' ✅'
                    keyboard_changed = True
            elif chosen_setting != UserSettings.TURN_ON_VOICE_MESSAGES:
                text = text.replace(' ✅', '')
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        if chosen_setting in ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']:
            user.settings[Model.CHAT_GPT][UserSettings.VOICE] = chosen_setting
            user.settings[Model.CLAUDE][UserSettings.VOICE] = chosen_setting
            user.settings[Model.GEMINI][UserSettings.VOICE] = chosen_setting
            user.settings[Model.GROK][UserSettings.VOICE] = chosen_setting
            user.settings[Model.PERPLEXITY][UserSettings.VOICE] = chosen_setting

            user.settings[Model.EIGHTIFY][UserSettings.VOICE] = chosen_setting
            user.settings[Model.GEMINI_VIDEO][UserSettings.VOICE] = chosen_setting
        else:
            new_setting = not user.settings[Model.CHAT_GPT][chosen_setting]
            user.settings[Model.CHAT_GPT][chosen_setting] = new_setting
            user.settings[Model.CLAUDE][chosen_setting] = new_setting
            user.settings[Model.GEMINI][chosen_setting] = new_setting
            user.settings[Model.GROK][chosen_setting] = new_setting
            user.settings[Model.PERPLEXITY][chosen_setting] = new_setting

            user.settings[Model.EIGHTIFY][chosen_setting] = new_setting
            user.settings[Model.GEMINI_VIDEO][chosen_setting] = new_setting

        await update_user(
            user_id, {
                'settings': user.settings,
            },
        )

        await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard))


async def handle_chats(message: Message, user_id: str, state: FSMContext, model: Optional[Model] = None):
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    all_chats = await get_chats_by_user_id(user_id)
    current_chat = await get_chat_by_user_id(user_id)

    text = get_localization(user_language_code).chats(
        current_chat.title,
        len(all_chats),
        user.daily_limits[Quota.ADDITIONAL_CHATS] + user.additional_usage_quota[Quota.ADDITIONAL_CHATS],
    )
    reply_markup = build_chats_keyboard(user_language_code, model)
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
    )


@settings_router.callback_query(lambda c: c.data.startswith('chat:'))
async def handle_chat_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'back':
        if len(callback_query.data.split(':')) == 3:
            chosen_model = cast(Model, callback_query.data.split(':')[2])
            human_model = get_human_model(chosen_model, user_language_code)
            reply_markup = build_settings_keyboard(
                language_code=user_language_code,
                model=chosen_model,
                model_type=get_model_type(chosen_model),
                settings=user.settings,
            )
            await callback_query.message.edit_text(
                text=get_localization(user_language_code).settings(human_model, chosen_model),
                reply_markup=reply_markup,
            )
        else:
            reply_markup = build_settings_choose_text_model_keyboard(user_language_code)
            await callback_query.message.edit_text(
                text=get_localization(user_language_code).SETTINGS_CHOOSE_MODEL,
                reply_markup=reply_markup,
            )
        return
    elif action == 'show':
        all_chats = await get_chats_by_user_id(user_id)
        text = ''
        for count, chat in enumerate(all_chats):
            text += f'\n{count + 1}. <b>{chat.title}</b>'

        await callback_query.message.answer(text=text)
    elif action == 'create':
        if user.daily_limits[Quota.ADDITIONAL_CHATS] + user.additional_usage_quota[Quota.ADDITIONAL_CHATS] > 0:
            reply_markup = build_create_chat_keyboard(user_language_code)

            await callback_query.message.answer(
                text=get_localization(user_language_code).TYPE_CHAT_NAME,
                reply_markup=reply_markup,
            )

            await state.set_state(Chats.waiting_for_chat_name)
        else:
            text = get_localization(user_language_code).CREATE_CHAT_FORBIDDEN
            reply_markup = build_buy_motivation_keyboard(user_language_code)
            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
            )
    elif action == 'switch':
        all_chats = await get_chats_by_user_id(user_id)

        if len(all_chats) > 1:
            current_chat = await get_chat_by_user_id(user_id)
            reply_markup = build_switch_chat_keyboard(user_language_code, current_chat.id, all_chats)

            await callback_query.message.answer(
                text=get_localization(user_language_code).SWITCH_CHAT,
                reply_markup=reply_markup,
            )
        else:
            text = get_localization(user_language_code).SWITCH_CHAT_FORBIDDEN
            reply_markup = build_buy_motivation_keyboard(user_language_code)
            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
            )
    elif action == 'reset':
        reply_keyboard = build_reset_chat_keyboard(user_language_code)
        await callback_query.message.answer(
            text=get_localization(user_language_code).RESET_CHAT_WARNING,
            reply_markup=reply_keyboard,
        )
    elif action == 'delete':
        all_chats = await get_chats_by_user_id(user_id)

        if len(all_chats) > 1:
            current_chat = await get_chat_by_user_id(user_id)
            reply_markup = build_delete_chat_keyboard(user_language_code, current_chat.id, all_chats)

            await callback_query.message.answer(
                text=get_localization(user_language_code).DELETE_CHAT,
                reply_markup=reply_markup,
            )
        else:
            text = get_localization(user_language_code).DELETE_CHAT_FORBIDDEN
            reply_markup = build_buy_motivation_keyboard(user_language_code)
            await callback_query.message.answer(
                text=text,
                reply_markup=reply_markup,
            )


@settings_router.callback_query(lambda c: c.data.startswith('switch_chat:'))
async def handle_switch_chat_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    chat_id = callback_query.data.split(':')[1]

    keyboard = callback_query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(':', 1)[1]

            if callback_data == chat_id:
                if '❌' in text:
                    text = text.replace(' ❌', ' ✅')
                    keyboard_changed = True
            else:
                text = text.replace(' ✅', ' ❌')
            new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        await update_user(user_id, {
            'current_chat_id': chat_id
        })

        await callback_query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard)
        )

        await callback_query.message.reply(
            text=get_localization(user_language_code).SWITCH_CHAT_SUCCESS,
            allow_sending_without_reply=True,
        )


@settings_router.callback_query(lambda c: c.data.startswith('delete_chat:'))
async def handle_delete_chat_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    chat_id = callback_query.data.split(':')[1]

    keyboard = callback_query.message.reply_markup.inline_keyboard

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(':', 1)[1]

            if callback_data != chat_id:
                new_row.append(InlineKeyboardButton(text=text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    await delete_chat(chat_id)

    await callback_query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(inline_keyboard=new_keyboard)
    )

    await callback_query.message.reply(
        text=get_localization(user_language_code).DELETE_CHAT_SUCCESS,
        allow_sending_without_reply=True,
    )


@settings_router.message(Chats.waiting_for_chat_name, F.text, ~F.text.startswith('/'))
async def chat_name_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    transaction = firebase.db.transaction()
    await create_new_chat(transaction, user, str(message.chat.id), message.text)

    await message.answer(get_localization(user_language_code).CREATE_CHAT_SUCCESS)

    await message.delete()

    await state.clear()


@settings_router.callback_query(lambda c: c.data.startswith('reset_chat:'))
async def handle_reset_chat_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'approve':
        await reset_chat(user.current_chat_id)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).RESET_CHAT_SUCCESS,
        )
