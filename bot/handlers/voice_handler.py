import math
import os
import tempfile
import uuid

import ffmpeg
from pydub import AudioSegment
from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.models.common import Quota, Currency, Model
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user
from bot.handlers.chat_gpt_handler import handle_chatgpt
from bot.handlers.dalle_handler import handle_dalle
from bot.integrations.openAI import get_response_speech_to_text
from bot.locales.main import get_localization

voice_router = Router()


async def download_file(url: str, destination: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(destination, 'wb') as f:
                    f.write(await response.read())


def convert_ogg_to_wav(input_path: str, output_path: str):
    ffmpeg.input(input_path).output(output_path).run()


async def process_voice_message(voice_url: str, user_id: str):
    with tempfile.TemporaryDirectory() as tempdir:
        unique_id = uuid.uuid4()
        ogg_path = os.path.join(tempdir, f"{unique_id}.ogg")
        wav_path = os.path.join(tempdir, f"{unique_id}.wav")

        await download_file(voice_url, ogg_path)

        convert_ogg_to_wav(ogg_path, wav_path)

        audio = AudioSegment.from_file(wav_path)
        audio_file = open(wav_path, "rb")
        text = await get_response_speech_to_text(audio_file)
        audio_file.close()

        total_price = 0.0001 * math.ceil(audio.duration_seconds)
        await write_transaction(user_id=user_id,
                                type=TransactionType.EXPENSE,
                                service=ServiceType.VOICE_MESSAGES,
                                amount=total_price,
                                currency=Currency.USD,
                                quantity=1)

        return text


@voice_router.message(F.voice)
async def handle_voice(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    if user.additional_usage_quota[Quota.VOICE_MESSAGES]:
        voice_file = await message.voice

        text = await process_voice_message(voice_file.file_path, user.id)

        await state.update_data(recognized_text=text)
        if user.current_model == Model.GPT3 or user.current_model == Model.GPT4:
            await handle_chatgpt(message, state)
        elif user.current_model == Model.DALLE3:
            await handle_dalle(message, state)
        await state.update_data(recognized_text=None)
    else:
        await message.answer(text=get_localization(user.language_code).VOICE_MESSAGES_FORBIDDEN)
