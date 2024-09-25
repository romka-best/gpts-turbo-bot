from datetime import datetime, timezone
from typing import Dict

from bot.database.main import firebase
from bot.database.models.feedback import Feedback


async def update_feedback(feedback_id: str, data: Dict):
    feedback_ref = firebase.db.collection(Feedback.COLLECTION_NAME).document(feedback_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await feedback_ref.update(data)