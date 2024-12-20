from google.generativeai import configure, GenerativeModel, GenerationConfig
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from bot.config import config
from bot.database.models.common import GeminiGPTVersion

configure(api_key=config.GEMINI_API_KEY.get_secret_value())


def get_default_max_tokens(model_version: GeminiGPTVersion) -> int:
    base = 1024
    if (
        model_version == GeminiGPTVersion.V1_Flash or
        model_version == GeminiGPTVersion.V1_Pro
    ):
        return base
    elif model_version == GeminiGPTVersion.V1_Ultra:
        return base * 2

    return base


async def get_response_message(
    model_version: GeminiGPTVersion,
    system_prompt: str,
    new_prompt: dict,
    history: list,
) -> dict:
    max_tokens = get_default_max_tokens(model_version)

    if model_version == GeminiGPTVersion.V1_Ultra:
        model_name = GeminiGPTVersion.V1_Pro
    else:
        model_name = model_version
    model = GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt,
    )
    chat = model.start_chat(
        history=history,
    )
    response = await chat.send_message_async(
        content=new_prompt,
        generation_config=GenerationConfig(
            max_output_tokens=max_tokens,
        ),
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    return {
        'finish_reason': response.candidates[-1].finish_reason,
        'message': response.text,
        'input_tokens': response.usage_metadata.prompt_token_count,
        'output_tokens': response.usage_metadata.candidates_token_count,
    }
