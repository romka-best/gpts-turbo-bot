from bot.database.models.common import Model
from bot.locales.main import get_localization
from bot.locales.types import LanguageCode


def get_info_by_model(model: Model, language_code: LanguageCode):
    info = None

    if model == Model.CHAT_GPT:
        info = get_localization(language_code).INFO_CHAT_GPT
    elif model == Model.CLAUDE:
        info = get_localization(language_code).INFO_CLAUDE
    elif model == Model.GEMINI:
        info = get_localization(language_code).INFO_GEMINI
    elif model == Model.GROK:
        info = get_localization(language_code).INFO_GROK
    elif model == Model.PERPLEXITY:
        info = get_localization(language_code).INFO_PERPLEXITY
    elif model == Model.DALL_E:
        info = get_localization(language_code).INFO_DALL_E
    elif model == Model.MIDJOURNEY:
        info = get_localization(language_code).INFO_MIDJOURNEY
    elif model == Model.STABLE_DIFFUSION:
        info = get_localization(language_code).INFO_STABLE_DIFFUSION
    elif model == Model.FLUX:
        info = get_localization(language_code).INFO_FLUX
    elif model == Model.LUMA_PHOTON:
        info = get_localization(language_code).INFO_LUMA_PHOTON
    elif model == Model.FACE_SWAP:
        info = get_localization(language_code).INFO_FACE_SWAP
    elif model == Model.PHOTOSHOP_AI:
        info = get_localization(language_code).INFO_PHOTOSHOP_AI
    elif model == Model.MUSIC_GEN:
        info = get_localization(language_code).INFO_MUSIC_GEN
    elif model == Model.SUNO:
        info = get_localization(language_code).INFO_SUNO
    elif model == Model.KLING:
        info = get_localization(language_code).INFO_KLING
    elif model == Model.RUNWAY:
        info = get_localization(language_code).INFO_RUNWAY
    elif model == Model.LUMA_RAY:
        info = get_localization(language_code).INFO_LUMA_RAY

    return info
