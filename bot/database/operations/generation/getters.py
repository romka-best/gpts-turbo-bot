from typing import Optional, List

from google.cloud.firestore_v1 import FieldFilter, Query

from bot.database.main import firebase
from bot.database.models.generation import Generation


async def get_generation(generation_id: str) -> Optional[Generation]:
    generation_ref = firebase.db.collection(Generation.COLLECTION_NAME).document(str(generation_id))
    generation = await generation_ref.get()

    if generation.exists:
        return Generation(**generation.to_dict())


async def get_generations() -> List[Generation]:
    generations_stream = firebase.db.collection(Generation.COLLECTION_NAME) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .stream()
    generations = [Generation(**generation.to_dict()) async for generation in generations_stream]

    return generations


async def get_generations_by_request_id(request_id: str) -> List[Generation]:
    generations_stream = firebase.db.collection(Generation.COLLECTION_NAME) \
        .where(filter=FieldFilter("request_id", "==", request_id)) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .stream()
    generations = [Generation(**generation.to_dict()) async for generation in generations_stream]

    return generations
