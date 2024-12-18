from bot.database.models.common import Model
from bot.locales.main import get_localization
from bot.locales.types import LanguageCode


def get_human_model(model: Model, language_code: LanguageCode):
    if model == Model.CHAT_GPT:
        human_model = get_localization(language_code).CHATGPT
    elif model == Model.CLAUDE:
        human_model = get_localization(language_code).CLAUDE
    elif model == Model.GEMINI:
        human_model = get_localization(language_code).GEMINI
    elif model == Model.EIGHTIFY:
        human_model = get_localization(language_code).EIGHTIFY
    elif model == Model.DALL_E:
        human_model = get_localization(language_code).DALL_E
    elif model == Model.MIDJOURNEY:
        human_model = get_localization(language_code).MIDJOURNEY
    elif model == Model.STABLE_DIFFUSION:
        human_model = get_localization(language_code).STABLE_DIFFUSION
    elif model == Model.FLUX:
        human_model = get_localization(language_code).FLUX
    elif model == Model.FACE_SWAP:
        human_model = get_localization(language_code).FACE_SWAP
    elif model == Model.PHOTOSHOP_AI:
        human_model = get_localization(language_code).PHOTOSHOP_AI
    elif model == Model.MUSIC_GEN:
        human_model = get_localization(language_code).MUSIC_GEN
    elif model == Model.SUNO:
        human_model = get_localization(language_code).SUNO
    elif model == Model.RUNWAY:
        human_model = get_localization(language_code).RUNWAY
    else:
        human_model = model

    return human_model
