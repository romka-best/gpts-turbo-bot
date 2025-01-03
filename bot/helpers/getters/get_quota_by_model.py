from bot.database.models.common import Model, Quota, ChatGPTVersion, ClaudeGPTVersion, GeminiGPTVersion


def get_quota_by_model(model: Model, version: str):
    if model == Model.CHAT_GPT:
        if version == ChatGPTVersion.V4_Omni_Mini:
            return Quota.CHAT_GPT4_OMNI_MINI
        elif version == ChatGPTVersion.V4_Omni:
            return Quota.CHAT_GPT4_OMNI
        elif version == ChatGPTVersion.V1_O_Mini:
            return Quota.CHAT_GPT_O_1_MINI
        elif version == ChatGPTVersion.V1_O:
            return Quota.CHAT_GPT_O_1
    elif model == Model.CLAUDE:
        if version == ClaudeGPTVersion.V3_Haiku:
            return Quota.CLAUDE_3_HAIKU
        elif version == ClaudeGPTVersion.V3_Sonnet:
            return Quota.CLAUDE_3_SONNET
        elif version == ClaudeGPTVersion.V3_Opus:
            return Quota.CLAUDE_3_OPUS
    elif model == Model.GEMINI:
        if version == GeminiGPTVersion.V2_Flash:
            return Quota.GEMINI_2_FLASH
        elif version == GeminiGPTVersion.V1_Pro:
            return Quota.GEMINI_1_PRO
        elif version == GeminiGPTVersion.V1_Ultra:
            return Quota.GEMINI_1_ULTRA
    elif model == Model.GROK:
        return Quota.GROK_2
    elif model == Model.PERPLEXITY:
        return Quota.PERPLEXITY
    elif model == Model.EIGHTIFY:
        return Quota.EIGHTIFY
    elif model == Model.GEMINI_VIDEO:
        return Quota.GEMINI_VIDEO
    elif model == Model.DALL_E:
        return Quota.DALL_E
    elif model == Model.MIDJOURNEY:
        return Quota.MIDJOURNEY
    elif model == Model.STABLE_DIFFUSION:
        return Quota.STABLE_DIFFUSION
    elif model == Model.FLUX:
        return Quota.FLUX
    elif model == Model.LUMA_PHOTON:
        return Quota.LUMA_PHOTON
    elif model == Model.FACE_SWAP:
        return Quota.FACE_SWAP
    elif model == Model.PHOTOSHOP_AI:
        return Quota.PHOTOSHOP_AI
    elif model == Model.MUSIC_GEN:
        return Quota.MUSIC_GEN
    elif model == Model.SUNO:
        return Quota.SUNO
    elif model == Model.KLING:
        return Quota.KLING
    elif model == Model.RUNWAY:
        return Quota.RUNWAY
    elif model == Model.LUMA_RAY:
        return Quota.LUMA_RAY
    else:
        raise NotImplementedError(f'User Model is not Implemented: {model}')
