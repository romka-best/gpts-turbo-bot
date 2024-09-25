from typing import Dict

import google.generativeai as genai
from google.generativeai import GenerationConfig

from bot.config import config
from bot.database.models.common import GeminiGPTVersion

genai.configure(api_key=config.GEMINI_API_KEY.get_secret_value())


def get_default_max_tokens(model_version: GeminiGPTVersion) -> int:
    base = 1024
    if (
        model_version == GeminiGPTVersion.V1_Flash or
        model_version == GeminiGPTVersion.V1_Pro
    ):
        return base

    return base


async def get_response_message(
    model_version: GeminiGPTVersion,
    system_prompt: str,
    new_prompt: dict,
    history: list,
) -> Dict:
    max_tokens = get_default_max_tokens(model_version)

    model = genai.GenerativeModel(
        model_name=model_version,
        system_instruction=system_prompt,
    )
    chat = model.start_chat(
        history=history,
    )
    response = await chat.send_message_async(
        content=new_prompt,
        generation_config=GenerationConfig(
            max_output_tokens=max_tokens,
        )
    )

    return {
        'finish_reason': response.candidates[-1].finish_reason,
        'message': response.text,
        'input_tokens': response.usage_metadata.prompt_token_count,
        'output_tokens': response.usage_metadata.candidates_token_count,
    }
