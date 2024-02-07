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

from bot.database.models.common import Quota, Currency, Model
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user
from bot.handlers.chat_gpt_handler import handle_chatgpt
from bot.handlers.dalle_handler import handle_dalle
from bot.handlers.face_swap_handler import handle_face_swap
from bot.handlers.music_gen_handler import handle_music_gen
from bot.integrations.openAI import get_response_speech_to_text
from bot.locales.main import get_localization
from bot.utils.is_already_processing import is_already_processing
from bot.utils.is_messages_limit_exceeded import is_messages_limit_exceeded
from bot.utils.is_time_limit_exceeded import is_time_limit_exceeded

voice_router = Router()


async def process_voice_message(bot: Bot, voice: File, user_id: str):
    unique_id = uuid.uuid4()
    with tempfile.TemporaryDirectory() as tempdir:
        wav_path = os.path.join(tempdir, f"{unique_id}.wav")

        voice_ogg = io.BytesIO()
        await bot.download_file(voice.file_path, voice_ogg)

        audio = AudioSegment.from_file(voice_ogg, format="ogg")

        audio_in_seconds = audio.duration_seconds

        audio.export(wav_path, format="wav")

        audio_file = open(wav_path, "rb")
        text = await get_response_speech_to_text(audio_file)
        audio_file.close()

        total_price = 0.0001 * math.ceil(audio_in_seconds)
        await write_transaction(
            user_id=user_id,
            type=TransactionType.EXPENSE,
            service=ServiceType.VOICE_MESSAGES,
            amount=total_price,
            currency=Currency.USD,
            quantity=1,
            details={
                'subtype': 'STT',
                'text': text,
            },
        )

        return text


@voice_router.message(F.voice)
async def handle_voice(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    if user.additional_usage_quota[Quota.VOICE_MESSAGES]:
        current_time = time.time()

        if user.current_model == Model.GPT3:
            user_quota = Quota.GPT3
        elif user.current_model == Model.GPT4:
            user_quota = Quota.GPT4
        elif user.current_model == Model.DALLE3:
            user_quota = Quota.DALLE3
        elif user.current_model == Model.FACE_SWAP:
            user_quota = Quota.FACE_SWAP
        elif user.current_model == Model.MUSIC_GEN:
            user_quota = Quota.MUSIC_GEN
        else:
            return

        need_exit = (
            await is_time_limit_exceeded(message, state, user, current_time) or
            await is_messages_limit_exceeded(message, user, user_quota) or
            await is_already_processing(message, state, user, current_time)
        )
        if need_exit:
            return

        voice_file = await message.bot.get_file(message.voice.file_id)

        text = await process_voice_message(message.bot, voice_file, user.id)

        await state.update_data(recognized_text=text)
        if user.current_model == Model.GPT3 or user.current_model == Model.GPT4:
            await handle_chatgpt(message, state, user, user_quota)
        elif user.current_model == Model.DALLE3:
            await handle_dalle(message, state, user)
        elif user.current_model == Model.FACE_SWAP:
            await handle_face_swap(message.bot, str(message.chat.id), state, user.id, text)
        elif user.current_model == Model.MUSIC_GEN:
            await handle_music_gen(message.bot, str(message.chat.id), state, user.id, text)
        await state.update_data(recognized_text=None)
    else:
        await message.answer(text=get_localization(user.language_code).VOICE_MESSAGES_FORBIDDEN)
