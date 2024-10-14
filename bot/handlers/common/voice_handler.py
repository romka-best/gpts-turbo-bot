import io
import math
import os
import tempfile
import time
import uuid

from pydub import AudioSegment
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, File

from bot.database.models.common import (
    Quota,
    Currency,
    Model,
    ChatGPTVersion,
    ClaudeGPTVersion,
    GeminiGPTVersion,
    MidjourneyAction,
)
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserSettings
from bot.database.operations.transaction.writers import write_transaction
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
from bot.integrations.openAI import get_response_speech_to_text
from bot.locales.main import get_localization, get_user_language
from bot.utils.is_already_processing import is_already_processing
from bot.utils.is_messages_limit_exceeded import is_messages_limit_exceeded
from bot.utils.is_time_limit_exceeded import is_time_limit_exceeded

voice_router = Router()


async def process_voice_message(bot: Bot, voice: File, user_id: str):
    unique_id = uuid.uuid4()
    with tempfile.TemporaryDirectory() as tempdir:
        wav_path = os.path.join(tempdir, f'{unique_id}.wav')

        voice_ogg = io.BytesIO()
        await bot.download_file(voice.file_path, voice_ogg)

        audio = AudioSegment.from_file(voice_ogg, format='ogg')

        audio_in_seconds = audio.duration_seconds

        audio.export(wav_path, format='wav')

        audio_file = open(wav_path, 'rb')
        text = await get_response_speech_to_text(audio_file)
        audio_file.close()

        total_price = 0.0001 * math.ceil(audio_in_seconds)
        await write_transaction(
            user_id=user_id,
            type=TransactionType.EXPENSE,
            service=ServiceType.VOICE_MESSAGES,
            amount=total_price,
            clear_amount=total_price,
            currency=Currency.USD,
            quantity=1,
            details={
                'subtype': 'STT',
                'text': text,
                'has_error': False,
            },
        )

        return text


@voice_router.message(F.voice)
async def handle_voice(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    if user.additional_usage_quota[Quota.VOICE_MESSAGES]:
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
            elif user.settings[user.current_model][UserSettings.VERSION] == GeminiGPTVersion.V1_Flash:
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

        voice_file = await message.bot.get_file(message.voice.file_id)

        text = await process_voice_message(message.bot, voice_file, user_id)

        await state.update_data(recognized_text=text)
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
            await handle_face_swap(message.bot, str(message.chat.id), state, user_id, text)
        elif user.current_model == Model.PHOTOSHOP_AI:
            await handle_photoshop_ai(message.bot, str(message.chat.id), state, user_id, text)
        elif user.current_model == Model.MUSIC_GEN:
            await handle_music_gen(message.bot, str(message.chat.id), state, user_id, text)
        elif user.current_model == Model.SUNO:
            await handle_suno(message.bot, str(message.chat.id), state, user_id)
        else:
            raise NotImplementedError(
                f'User model is not found: {user.current_model}'
            )

        await state.update_data(recognized_text=None)
    else:
        await message.answer(text=get_localization(user_language_code).VOICE_MESSAGES_FORBIDDEN)
