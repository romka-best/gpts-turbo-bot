from bot.database.models.common import Model
from bot.database.models.generation import Generation, GenerationStatus, GenerationReaction


async def create_generation_object(
    id: str,
    request_id: str,
    model: Model,
    result='',
    has_error=False,
    status=GenerationStatus.STARTED,
    reaction=GenerationReaction.NONE,
    seconds=0,
    details=None,
) -> Generation:
    return Generation(
        id=id,
        request_id=request_id,
        model=model,
        result=result,
        has_error=has_error,
        status=status,
        reaction=reaction,
        seconds=seconds,
        details=details,
    )
