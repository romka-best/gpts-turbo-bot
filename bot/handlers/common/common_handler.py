import asyncio

from aiogram import Router
from aiogram.filters import Command, CommandStart, ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from bot.config import config, MessageEffect, MessageSticker
from bot.database.main import firebase
from bot.database.models.common import (
    Model,
    Quota,
    UTM,
    ChatGPTVersion,
    ClaudeGPTVersion,
    GeminiGPTVersion,
    GrokGPTVersion,
)
from bot.database.models.generation import Generation
from bot.database.models.user import UserSettings
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.user.getters import get_user, get_count_of_users_by_referral
from bot.database.operations.user.initialize_user_for_the_first_time import initialize_user_for_the_first_time
from bot.database.operations.user.updaters import update_user
from bot.handlers.ai.chat_gpt_handler import handle_chatgpt
from bot.handlers.ai.claude_handler import handle_claude
from bot.handlers.ai.face_swap_handler import handle_face_swap
from bot.handlers.ai.gemini_handler import handle_gemini
from bot.handlers.ai.grok_handler import handle_grok
from bot.handlers.ai.model_handler import handle_model
from bot.handlers.ai.music_gen_handler import handle_music_gen
from bot.handlers.ai.photoshop_ai_handler import handle_photoshop_ai
from bot.handlers.ai.suno_handler import handle_suno
from bot.handlers.common.catalog_handler import handle_catalog_prompts
from bot.handlers.payment.bonus_handler import handle_bonus
from bot.handlers.payment.payment_handler import handle_subscribe, handle_package
from bot.helpers.getters.get_quota_by_model import get_quota_by_model
from bot.helpers.getters.get_switched_to_ai_model import get_switched_to_ai_model
from bot.helpers.updaters.update_daily_limits import update_user_daily_limits
from bot.keyboards.ai.model import build_switched_to_ai_keyboard
from bot.keyboards.common.common import (
    build_start_keyboard,
    build_start_chosen_keyboard,
    build_error_keyboard,
    build_time_limit_exceeded_chosen_keyboard,
)
from bot.locales.main import get_localization, get_user_language

common_router = Router()


@common_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    tasks = []
    params = message.text.split()
    user_utm = {}
    utm = [value for key, value in vars(UTM).items() if not key.startswith('__')]

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    if not user:
        default_quota = Quota.CHAT_GPT4_OMNI_MINI
        referred_by = None
        referred_by_user = None
        if len(params) > 1:
            sub_params = params[1].split('_')
            for sub_param in sub_params:
                if '-' not in sub_param:
                    continue

                sub_param_key, sub_param_value = sub_param.split('-')
                if sub_param_key == 'r' or sub_param_key == 'referral':
                    referred_by = sub_param_value
                    referred_by_user = await get_user(referred_by)
                    referred_by_user_language_code = await get_user_language(referred_by, state.storage)

                    if referred_by_user:
                        count_of_referred_users = await get_count_of_users_by_referral(referred_by_user.id)
                        if count_of_referred_users > 40:
                            text = get_localization(referred_by_user_language_code).BONUS_REFERRAL_LIMIT_ERROR
                            tasks.append(message.bot.send_message(
                                chat_id=referred_by_user.telegram_chat_id,
                                text=text,
                                message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.CONGRATS),
                                disable_notification=True,
                            ))
                        else:
                            added_to_balance = 25.00
                            referred_by_user.balance += added_to_balance
                            await update_user(referred_by_user.id, {
                                'balance': referred_by_user.balance,
                            })

                            text = get_localization(referred_by_user_language_code).BONUS_REFERRAL_SUCCESS
                            tasks.append(message.bot.send_message(
                                chat_id=referred_by_user.telegram_chat_id,
                                text=text,
                                message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.CONGRATS),
                                disable_notification=True,
                            ))
                elif sub_param_key == 'model' and sub_param_value in [
                    'chatgpt4omnimini',
                    'chatgpt4omni',
                    'chatgpto1mini',
                    'chatgpto1',
                    'claude3haiku',
                    'claude3sonnet',
                    'claude3opus',
                    'gemini2flash',
                    'gemini1pro',
                    'gemini1ultra',
                    'grok',
                    'perplexity',
                    'eightify',
                    'geminivideo',
                    'dalle',
                    'midjourney',
                    'stablediffusion',
                    'flux',
                    'lumaphoton',
                    'faceswap',
                    'photoshopai',
                    'suno',
                    'musicgen',
                    'kling',
                    'runway',
                    'lumaray',
                ]:
                    if sub_param_value == 'chatgpt4omnimini':
                        default_quota = Quota.CHAT_GPT4_OMNI_MINI
                    elif sub_param_value == 'chatgpt4omni':
                        default_quota = Quota.CHAT_GPT4_OMNI
                    elif sub_param_value == 'chatgpto1mini':
                        default_quota = Quota.CHAT_GPT_O_1_MINI
                    elif sub_param_value == 'chatgpto1':
                        default_quota = Quota.CHAT_GPT_O_1
                    elif sub_param_value == 'claude3haiku':
                        default_quota = Quota.CLAUDE_3_HAIKU
                    elif sub_param_value == 'claude3sonnet':
                        default_quota = Quota.CLAUDE_3_SONNET
                    elif sub_param_value == 'claude3opus':
                        default_quota = Quota.CLAUDE_3_OPUS
                    elif sub_param_value == 'gemini2flash':
                        default_quota = Quota.GEMINI_2_FLASH
                    elif sub_param_value == 'gemini1pro':
                        default_quota = Quota.GEMINI_1_PRO
                    elif sub_param_value == 'gemini1ultra':
                        default_quota = Quota.GEMINI_1_ULTRA
                    elif sub_param_value == 'grok':
                        default_quota = Quota.GROK_2
                    elif sub_param_value == 'perplexity':
                        default_quota = Quota.PERPLEXITY
                    elif sub_param_value == 'eightify':
                        default_quota = Quota.EIGHTIFY
                    elif sub_param_value == 'geminivideo':
                        default_quota = Quota.GEMINI_VIDEO
                    elif sub_param_value == 'dalle':
                        default_quota = Quota.DALL_E
                    elif sub_param_value == 'midjourney':
                        default_quota = Quota.MIDJOURNEY
                    elif sub_param_value == 'stablediffusion':
                        default_quota = Quota.STABLE_DIFFUSION
                    elif sub_param_value == 'flux':
                        default_quota = Quota.FLUX
                    elif sub_param_value == 'lumaphoton':
                        default_quota = Quota.LUMA_PHOTON
                    elif sub_param_value == 'faceswap':
                        default_quota = Quota.FACE_SWAP
                    elif sub_param_value == 'photoshopai':
                        default_quota = Quota.PHOTOSHOP_AI
                    elif sub_param_value == 'suno':
                        default_quota = Quota.SUNO
                    elif sub_param_value == 'musicgen':
                        default_quota = Quota.MUSIC_GEN
                    elif sub_param_value == 'kling':
                        default_quota = Quota.KLING
                    elif sub_param_value == 'runway':
                        default_quota = Quota.RUNWAY
                    elif sub_param_value == 'lumaray':
                        default_quota = Quota.LUMA_RAY
                elif sub_param_key in utm:
                    user_utm[sub_param_key] = sub_param_value.lower()

        language_code = message.from_user.language_code
        await state.storage.redis.set(f'user:{user_id}:language', language_code)

        chat_title = get_localization(language_code).CHAT_DEFAULT_TITLE
        transaction = firebase.db.transaction()
        user = await initialize_user_for_the_first_time(
            transaction,
            message.from_user,
            str(message.chat.id),
            chat_title,
            referred_by,
            bool(referred_by_user),
            default_quota,
            user_utm,
        )
    elif user and user.is_blocked:
        user.is_blocked = False
        await update_user(user.id, {
            'is_blocked': user.is_blocked,
        })

        batch = firebase.db.batch()
        await update_user_daily_limits(message.bot, user, batch, state.storage)
        await batch.commit()
    elif user and len(params) > 1:
        sub_params = params[1].split('_')
        for sub_param in sub_params:
            if '-' not in sub_param:
                continue

            sub_param_key, sub_param_value = sub_param.split('-')
            if sub_param_key in utm:
                user_utm[sub_param_key] = sub_param_value.lower()

    user_language_code = await get_user_language(user_id, state.storage)

    await message.answer_sticker(
        sticker=config.MESSAGE_STICKERS.get(MessageSticker.HELLO),
    )

    await message.answer(
        text=get_localization(user_language_code).START_INFO,
        reply_markup=build_start_keyboard(user_language_code),
        message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.CONGRATS),
    )

    await asyncio.sleep(5)

    answered_message = await message.answer(
        text=await get_switched_to_ai_model(
            user,
            get_quota_by_model(user.current_model, user.settings[user.current_model][UserSettings.VERSION]),
            user_language_code,
        ),
        reply_markup=build_switched_to_ai_keyboard(user_language_code, user.current_model),
        message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.FIRE),
    )

    await message.bot.unpin_all_chat_messages(user.telegram_chat_id)
    await message.bot.pin_chat_message(user.telegram_chat_id, answered_message.message_id)

    if user.current_model == Model.EIGHTIFY:
        await message.answer(
            text=get_localization(user_language_code).EIGHTIFY_INFO,
        )
    elif user.current_model == Model.GEMINI_VIDEO:
        await message.answer(
            text=get_localization(user_language_code).GEMINI_VIDEO_INFO,
        )
    elif user.current_model == Model.FACE_SWAP:
        await handle_face_swap(
            bot=message.bot,
            chat_id=user.telegram_chat_id,
            state=state,
            user_id=user.id,
        )
    elif user.current_model == Model.PHOTOSHOP_AI:
        await handle_photoshop_ai(
            bot=message.bot,
            chat_id=user.telegram_chat_id,
            state=state,
            user_id=user.id,
        )
    elif user.current_model == Model.MUSIC_GEN:
        await handle_music_gen(
            bot=message.bot,
            chat_id=user.telegram_chat_id,
            state=state,
            user_id=user.id,
        )
    elif user.current_model == Model.SUNO:
        await handle_suno(
            bot=message.bot,
            chat_id=user.telegram_chat_id,
            state=state,
            user_id=user.id,
        )

    if len(tasks) > 0:
        await asyncio.gather(*tasks)


@common_router.callback_query(lambda c: c.data.startswith('start:'))
async def start_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    if action == 'quick_guide':
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).START_QUICK_GUIDE,
            reply_markup=build_start_chosen_keyboard(user_language_code),
        )
    elif action == 'additional_features':
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).START_ADDITIONAL_FEATURES,
            reply_markup=build_start_chosen_keyboard(user_language_code),
        )
    else:
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).START_INFO,
            reply_markup=build_start_keyboard(user_language_code),
            message_effect_id=config.MESSAGE_EFFECTS.get(MessageEffect.CONGRATS),
        )


@common_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated):
    user = await get_user(str(event.from_user.id))
    user.is_blocked = True
    await update_user(user.id, {
        'is_blocked': user.is_blocked,
    })


@common_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated, state: FSMContext):
    user = await get_user(str(event.from_user.id))
    user.is_blocked = False
    await update_user(user.id, {
        'is_blocked': user.is_blocked,
    })

    batch = firebase.db.batch()
    await update_user_daily_limits(event.bot, user, batch, state.storage)
    await batch.commit()


@common_router.message(Command('help'))
async def handle_help(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    text = get_localization(user_language_code).HELP_INFO
    reply_markup = build_error_keyboard(user_language_code)
    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


@common_router.message(Command('terms'))
async def terms(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    await message.answer(text=get_localization(user_language_code).TERMS_LINK)


@common_router.callback_query(lambda c: c.data.startswith('continue_generation:'))
async def handle_continue_generation_choose_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'continue':
        await state.update_data(recognized_text=get_localization(user_language_code).MODEL_CONTINUE_GENERATING)

        if user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V4_Omni_Mini:
            user_quota = Quota.CHAT_GPT4_OMNI_MINI
        elif user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V4_Omni:
            user_quota = Quota.CHAT_GPT4_OMNI
        elif user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V1_O_Mini:
            user_quota = Quota.CHAT_GPT_O_1_MINI
        elif user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V1_O:
            user_quota = Quota.CHAT_GPT_O_1
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Haiku:
            user_quota = Quota.CLAUDE_3_HAIKU
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Sonnet:
            user_quota = Quota.CLAUDE_3_SONNET
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Opus:
            user_quota = Quota.CLAUDE_3_OPUS
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V2_Flash:
            user_quota = Quota.GEMINI_2_FLASH
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Pro:
            user_quota = Quota.GEMINI_1_PRO
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Ultra:
            user_quota = Quota.GEMINI_1_ULTRA
        elif user.settings[user.current_model][UserSettings.VERSION] == GrokGPTVersion.V2:
            user_quota = Quota.GROK_2
        else:
            raise NotImplementedError(
                f'AI version is not defined: {user.settings[user.current_model][UserSettings.VERSION]}'
            )

        if user_quota in [
            Quota.CHAT_GPT4_OMNI_MINI,
            Quota.CHAT_GPT4_OMNI,
            Quota.CHAT_GPT_O_1_MINI,
            Quota.CHAT_GPT_O_1,
        ]:
            await handle_chatgpt(callback_query.message, state, user, user_quota)
        elif user_quota in [
            Quota.CLAUDE_3_HAIKU,
            Quota.CLAUDE_3_SONNET,
            Quota.CLAUDE_3_OPUS,
        ]:
            await handle_claude(callback_query.message, state, user, user_quota)
        elif user_quota in [
            Quota.GEMINI_2_FLASH,
            Quota.GEMINI_1_PRO,
            Quota.GEMINI_1_ULTRA,
        ]:
            await handle_gemini(callback_query.message, state, user, user_quota)
        elif user_quota == Quota.GROK_2:
            await handle_grok(callback_query.message, state, user)

        await callback_query.message.edit_reply_markup(reply_markup=None)
        await state.update_data(recognized_text=None)

    await state.clear()


@common_router.callback_query(lambda c: c.data.startswith('reaction:'))
async def reaction_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    reaction, generation_id = callback_query.data.split(':')[1], callback_query.data.split(':')[2]
    await update_generation(generation_id, {
        'reaction': reaction,
    })

    if callback_query.message.caption:
        await callback_query.message.edit_reply_markup(
            reply_markup=None,
        )
    else:
        await callback_query.message.edit_caption(
            caption=Generation.get_reaction_emojis()[reaction],
            reply_markup=None,
        )


@common_router.callback_query(lambda c: c.data.startswith('limit_exceeded:'))
async def limit_exceeded_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    if action == 'change_ai_model':
        await handle_model(callback_query.message, state, str(callback_query.from_user.id))
    elif action == 'open_bonus_info':
        await handle_bonus(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'open_buy_subscriptions_info':
        await handle_subscribe(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'open_buy_packages_info':
        await handle_package(callback_query.message, str(callback_query.from_user.id), state)


@common_router.callback_query(lambda c: c.data.startswith('buy_motivation:'))
async def buy_motivation_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    if action == 'open_bonus_info':
        await handle_bonus(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'open_buy_subscriptions_info':
        await handle_subscribe(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'open_buy_packages_info':
        await handle_package(callback_query.message, str(callback_query.from_user.id), state)


@common_router.callback_query(lambda c: c.data.startswith('time_limit_exceeded:'))
async def time_limit_exceeded_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'remove_restriction':
        text = get_localization(user_language_code).REMOVE_RESTRICTION_INFO
        reply_markup = build_time_limit_exceeded_chosen_keyboard(user_language_code)
        await callback_query.message.reply(
            text=text,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )


@common_router.callback_query(lambda c: c.data.startswith('notify_about_quota:'))
async def notify_about_quota_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    if action == 'examples':
        await handle_catalog_prompts(
            callback_query.message,
            str(callback_query.from_user.id),
            state,
            False,
        )


@common_router.callback_query(lambda c: c.data.startswith('suggestions:'))
async def suggestions_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    action = callback_query.data.split(':')[1]
    if action == 'change_ai_model':
        await handle_model(callback_query.message, state, str(callback_query.from_user.id))


@common_router.callback_query(lambda c: c.data.endswith(':close'))
async def handle_close_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    if isinstance(callback_query.message, Message):
        await callback_query.message.delete()


@common_router.callback_query(lambda c: c.data.endswith(':cancel'))
async def handle_cancel_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    if isinstance(callback_query.message, Message):
        await callback_query.message.delete()

    await state.clear()
