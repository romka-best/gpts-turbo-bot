import time

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.models.common import (
    Model,
    Quota,
    ChatGPTVersion,
    ClaudeGPTVersion,
    GeminiGPTVersion,
    MidjourneyAction,
)
from bot.database.models.user import UserSettings
from bot.database.operations.user.getters import get_user
from bot.handlers.ai.chat_gpt_handler import handle_chatgpt
from bot.handlers.ai.claude_handler import handle_claude
from bot.handlers.ai.dalle_handler import handle_dall_e
from bot.handlers.ai.face_swap_handler import handle_face_swap
from bot.handlers.ai.flux_handler import handle_flux
from bot.handlers.ai.gemini_handler import handle_gemini
from bot.handlers.ai.midjourney_handler import handle_midjourney
from bot.handlers.ai.music_gen_handler import handle_music_gen
from bot.handlers.ai.photoshop_ai_handler import handle_photoshop_ai
from bot.handlers.ai.stable_diffusion_handler import handle_stable_diffusion
from bot.handlers.ai.suno_handler import handle_suno
from bot.handlers.common.common_handler import handle_help
from bot.utils.is_already_processing import is_already_processing
from bot.utils.is_messages_limit_exceeded import is_messages_limit_exceeded
from bot.utils.is_time_limit_exceeded import is_time_limit_exceeded

text_router = Router()


@text_router.message(F.text, ~F.text.startswith('/'))
async def handle_text(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    current_time = time.time()

    if user.current_model == Model.CHAT_GPT:
        if user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V4_Omni_Mini:
            user_quota = Quota.CHAT_GPT4_OMNI_MINI
        elif user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V4_Omni:
            user_quota = Quota.CHAT_GPT4_OMNI
        elif user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V1_O_Mini:
            user_quota = Quota.CHAT_GPT_O_1_MINI
        elif user.settings[user.current_model][UserSettings.VERSION] == ChatGPTVersion.V1_O_Preview:
            user_quota = Quota.CHAT_GPT_O_1_PREVIEW
        else:
            raise NotImplementedError(
                f'User quota is not implemented: {user.settings[user.current_model][UserSettings.VERSION]}'
            )
    elif user.current_model == Model.CLAUDE:
        if user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Haiku:
            user_quota = Quota.CLAUDE_3_HAIKU
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Sonnet:
            user_quota = Quota.CLAUDE_3_SONNET
        elif user.settings[user.current_model][UserSettings.VERSION] == ClaudeGPTVersion.V3_Opus:
            user_quota = Quota.CLAUDE_3_OPUS
        else:
            raise NotImplementedError(
                f'User quota is not implemented: {user.settings[user.current_model][UserSettings.VERSION]}'
            )
    elif user.current_model == Model.GEMINI:
        if user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Flash:
            user_quota = Quota.GEMINI_1_FLASH
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Pro:
            user_quota = Quota.GEMINI_1_PRO
        elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Ultra:
            user_quota = Quota.GEMINI_1_ULTRA
        else:
            raise NotImplementedError(
                f'User quota is not implemented: {user.settings[user.current_model][UserSettings.VERSION]}'
            )
    elif user.current_model == Model.DALL_E:
        user_quota = Quota.DALL_E
    elif user.current_model == Model.MIDJOURNEY:
        user_quota = Quota.MIDJOURNEY
    elif user.current_model == Model.STABLE_DIFFUSION:
        user_quota = Quota.STABLE_DIFFUSION
    elif user.current_model == Model.FLUX:
        user_quota = Quota.FLUX
    elif user.current_model == Model.FACE_SWAP:
        user_quota = Quota.FACE_SWAP
    elif user.current_model == Model.PHOTOSHOP_AI:
        user_quota = Quota.PHOTOSHOP_AI
    elif user.current_model == Model.MUSIC_GEN:
        user_quota = Quota.MUSIC_GEN
    elif user.current_model == Model.SUNO:
        user_quota = Quota.SUNO
    else:
        raise NotImplementedError(
            f'User model is not found: {user.current_model}'
        )

    need_exit = (
        await is_already_processing(message, state, current_time) or
        await is_messages_limit_exceeded(message, state, user, user_quota) or
        await is_time_limit_exceeded(message, state, user, current_time)
    )
    if need_exit:
        return
    await state.update_data(last_request_time=current_time)

    if user.current_model == Model.CHAT_GPT:
        await handle_chatgpt(message, state, user, user_quota)
    elif user.current_model == Model.CLAUDE:
        await handle_claude(message, state, user, user_quota)
    elif user.current_model == Model.GEMINI:
        await handle_gemini(message, state, user, user_quota)
    elif user.current_model == Model.DALL_E:
        await handle_dall_e(message, state, user)
    elif user.current_model == Model.MIDJOURNEY:
        await handle_midjourney(message, state, user, message.text, MidjourneyAction.IMAGINE)
    elif user.current_model == Model.STABLE_DIFFUSION:
        await handle_stable_diffusion(message, state, user)
    elif user.current_model == Model.FLUX:
        await handle_flux(message, state, user)
    elif user.current_model == Model.FACE_SWAP:
        await handle_face_swap(message.bot, str(message.chat.id), state, user.id, message.text)
    elif user.current_model == Model.PHOTOSHOP_AI:
        await handle_photoshop_ai(message.bot, str(message.chat.id), state, user.id, message.text)
    elif user.current_model == Model.MUSIC_GEN:
        await handle_music_gen(message.bot, str(message.chat.id), state, user.id, message.text)
    elif user.current_model == Model.SUNO:
        await handle_suno(message.bot, str(message.chat.id), state, user.id)
    else:
        raise NotImplementedError(
            f'User model is not found: {user.current_model}'
        )


@text_router.message(F.text, F.text.startswith('/'))
async def handle_unrecognized_command(message: Message, state: FSMContext):
    await handle_help(message, state)
