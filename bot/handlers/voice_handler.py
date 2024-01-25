import io
import math
import os
import tempfile
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
from bot.integrations.openAI import get_response_speech_to_text
from bot.locales.main import get_localization

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
        await write_transaction(user_id=user_id,
                                type=TransactionType.EXPENSE,
                                service=ServiceType.VOICE_MESSAGES,
                                amount=total_price,
                                currency=Currency.USD,
                                quantity=1,
                                details={
                                    'subtype': 'STT',
                                    'text': text,
                                })

        return text


@voice_router.message(F.voice)
async def handle_voice(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    if user.additional_usage_quota[Quota.VOICE_MESSAGES]:
        voice_file = await message.bot.get_file(message.voice.file_id)

        text = await process_voice_message(message.bot, voice_file, user.id)

        await state.update_data(recognized_text=text)
        if user.current_model == Model.GPT3:
            await handle_chatgpt(message, state, user, Quota.GPT3)
        elif user.current_model == Model.GPT4:
            await handle_chatgpt(message, state, user, Quota.GPT4)
        elif user.current_model == Model.DALLE3:
            await handle_dalle(message, state, user, Quota.DALLE3)
        await state.update_data(recognized_text=None)
    else:
        await message.answer(text=get_localization(user.language_code).VOICE_MESSAGES_FORBIDDEN)
