from bot.database.models.common import Model, ChatGPTVersion, ClaudeGPTVersion, GeminiGPTVersion
from bot.locales.main import get_localization


def get_switched_to_ai_model(model: Model, version: str, language_code: str):
    text = None

    if model == Model.CHAT_GPT:
        if version == ChatGPTVersion.V4_Omni_Mini:
            text = get_localization(language_code).SWITCHED_TO_CHATGPT4_OMNI_MINI
        elif version == ChatGPTVersion.V4_Omni:
            text = get_localization(language_code).SWITCHED_TO_CHATGPT4_OMNI
        elif version == ChatGPTVersion.V1_O_Mini:
            text = get_localization(language_code).SWITCHED_TO_CHAT_GPT_O_1_MINI
        elif version == ChatGPTVersion.V1_O_Preview:
            text = get_localization(language_code).SWITCHED_TO_CHAT_GPT_O_1_PREVIEW
    elif model == Model.CLAUDE:
        if version == ClaudeGPTVersion.V3_Haiku:
            text = get_localization(language_code).SWITCHED_TO_CLAUDE_3_HAIKU
        elif version == ClaudeGPTVersion.V3_Sonnet:
            text = get_localization(language_code).SWITCHED_TO_CLAUDE_3_SONNET
        elif version == ClaudeGPTVersion.V3_Opus:
            text = get_localization(language_code).SWITCHED_TO_CLAUDE_3_OPUS
    elif model == Model.GEMINI:
        if version == GeminiGPTVersion.V1_Flash:
            text = get_localization(language_code).SWITCHED_TO_GEMINI_1_FLASH
        elif version == GeminiGPTVersion.V1_Pro:
            text = get_localization(language_code).SWITCHED_TO_GEMINI_1_PRO
        elif version == GeminiGPTVersion.V1_Ultra:
            text = get_localization(language_code).SWITCHED_TO_GEMINI_1_ULTRA
    elif model == Model.DALL_E:
        text = get_localization(language_code).SWITCHED_TO_DALL_E
    elif model == Model.MIDJOURNEY:
        text = get_localization(language_code).SWITCHED_TO_MIDJOURNEY
    elif model == Model.STABLE_DIFFUSION:
        text = get_localization(language_code).SWITCHED_TO_STABLE_DIFFUSION
    elif model == Model.FLUX:
        text = get_localization(language_code).SWITCHED_TO_FLUX
    elif model == Model.FACE_SWAP:
        text = get_localization(language_code).SWITCHED_TO_FACE_SWAP
    elif model == Model.PHOTOSHOP_AI:
        text = get_localization(language_code).SWITCHED_TO_PHOTOSHOP_AI
    elif model == Model.MUSIC_GEN:
        text = get_localization(language_code).SWITCHED_TO_MUSIC_GEN
    elif model == Model.SUNO:
        text = get_localization(language_code).SWITCHED_TO_SUNO

    return text
