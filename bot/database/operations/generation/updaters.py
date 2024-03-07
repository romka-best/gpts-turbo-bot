from datetime import datetime, timezone
from typing import Dict

from bot.database.main import firebase
from bot.database.models.generation import Generation


async def update_generation(generation_id: str, data: Dict):
    generation_ref = firebase.db.collection(Generation.COLLECTION_NAME).document(generation_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await generation_ref.update(data)
