from bot.database.models.common import Model
from bot.locales.main import get_localization


def get_info_by_model(model: Model, language_code: str):
    info = None

    if model == Model.CHAT_GPT:
        info = get_localization(language_code).INFO_CHATGPT
    elif model == Model.CLAUDE:
        info = get_localization(language_code).INFO_CLAUDE
    elif model == Model.GEMINI:
        info = get_localization(language_code).INFO_GEMINI
    elif model == Model.DALL_E:
        info = get_localization(language_code).INFO_DALL_E
    elif model == Model.MIDJOURNEY:
        info = get_localization(language_code).INFO_MIDJOURNEY
    elif model == Model.STABLE_DIFFUSION:
        info = get_localization(language_code).INFO_STABLE_DIFFUSION
    elif model == Model.FLUX:
        info = get_localization(language_code).INFO_FLUX
    elif model == Model.FACE_SWAP:
        info = get_localization(language_code).INFO_FACE_SWAP
    elif model == Model.PHOTOSHOP_AI:
        info = get_localization(language_code).INFO_PHOTOSHOP_AI
    elif model == Model.MUSIC_GEN:
        info = get_localization(language_code).INFO_MUSIC_GEN
    elif model == Model.SUNO:
        info = get_localization(language_code).INFO_SUNO

    return info
