import asyncio
from functools import partial
from typing import Dict, BinaryIO

import openai

from bot.config import config
from bot.database.models.common import Model

client = openai.OpenAI(api_key=config.OPENAI_API_KEY.get_secret_value())


def get_default_max_tokens(model: str) -> int:
    base = 1024
    if model == Model.GPT3 or model == Model.GPT4:
        return base

    return base


async def get_response_message(current_model: str, history: list) -> Dict:
    max_tokens = get_default_max_tokens(current_model)

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        partial(
            client.chat.completions.create,
            model=current_model,
            messages=history,
            max_tokens=max_tokens
        )
    )

    return {
        "finish_reason": response.choices[0].finish_reason,
        "message": response.choices[0].message,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens
    }


async def get_response_image(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        partial(
            client.images.generate,
            model=Model.DALLE3,
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
    )

    return response.data[0].url


async def get_response_speech_to_text(audio_file: BinaryIO) -> str:
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        partial(
            client.audio.transcriptions.create,
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    )

    return response


async def get_response_text_to_speech(text: str, voice='alloy'):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        partial(
            client.audio.speech.create,
            model="tts-1",
            voice=voice,
            response_format="opus",
            input=text
        )
    )

    return response
