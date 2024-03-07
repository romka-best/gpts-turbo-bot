from typing import Optional

from bot.database.main import firebase
from bot.database.models.feedback import Feedback


async def get_feedback(feedback_id: str) -> Optional[Feedback]:
    feedback_ref = firebase.db.collection(Feedback.COLLECTION_NAME).document(feedback_id)
    feedback = await feedback_ref.get()

    if feedback.exists:
        return Feedback(**feedback.to_dict())
