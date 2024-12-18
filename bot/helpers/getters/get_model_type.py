from bot.database.models.common import Model, ModelType


def get_model_type(model: Model):
    if (
        model == Model.CHAT_GPT or
        model == Model.CLAUDE or
        model == Model.GEMINI
    ):
        return ModelType.TEXT
    elif model == Model.EIGHTIFY:
        return ModelType.SUMMARY
    elif (
        model == Model.DALL_E or
        model == Model.MIDJOURNEY or
        model == Model.STABLE_DIFFUSION or
        model == Model.FLUX or
        model == Model.FACE_SWAP or
        model == Model.PHOTOSHOP_AI
    ):
        return ModelType.IMAGE
    elif model == Model.MUSIC_GEN or model == Model.SUNO:
        return ModelType.MUSIC
    elif model == Model.RUNWAY:
        return ModelType.VIDEO
