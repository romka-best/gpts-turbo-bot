from datetime import datetime, timezone
from typing import Optional, Dict, List

from google.cloud.firestore import Query

from bot.database.main import firebase
from bot.database.models.common import Model
from bot.database.models.generation import Generation, GenerationReaction, GenerationStatus


async def get_generation(generation_id: str) -> Optional[Generation]:
    generation_ref = firebase.db.collection("generations").document(str(generation_id))
    generation = await generation_ref.get()

    if generation.exists:
        return Generation(**generation.to_dict())


async def get_generations_by_request_id(request_id: str) -> List[Generation]:
    generations_stream = firebase.db.collection("generations") \
        .where("request_id", "==", request_id) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .stream()
    generations = [Generation(**generation.to_dict()) async for generation in generations_stream]

    return generations


async def create_generation_object(id: str,
                                   request_id: str,
                                   model: Model,
                                   result="",
                                   has_error=False,
                                   status=GenerationStatus.STARTED,
                                   reaction=GenerationReaction.NONE,
                                   seconds=0,
                                   details=None) -> Generation:
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


async def write_generation(id: Optional[str],
                           request_id: str,
                           model: Model,
                           result="",
                           has_error=False,
                           status=GenerationStatus.STARTED,
                           reaction=GenerationReaction.NONE,
                           seconds=0,
                           details=None) -> Generation:
    if not id:
        id = firebase.db.collection('generations').document().id

    generation = await create_generation_object(id,
                                                request_id,
                                                model,
                                                result,
                                                has_error,
                                                status,
                                                reaction,
                                                seconds,
                                                details)
    await firebase.db.collection('generations').document(id).set(
        generation.to_dict()
    )

    return generation


async def update_generation(generation_id: str, data: Dict):
    generation_ref = firebase.db.collection('generations').document(generation_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await generation_ref.update(data)
