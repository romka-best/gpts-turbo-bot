from typing import Optional, List

from google.cloud.firestore_v1 import FieldFilter

from bot.database.main import firebase
from bot.database.models.feedback import Feedback


async def get_feedback(feedback_id: str) -> Optional[Feedback]:
    feedback_ref = firebase.db.collection(Feedback.COLLECTION_NAME).document(feedback_id)
    feedback = await feedback_ref.get()

    if feedback.exists:
        return Feedback(**feedback.to_dict())


async def get_feedbacks_by_user_id(user_id: str) -> List[Feedback]:
    feedbacks_stream = firebase.db.collection(Feedback.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
        .stream()
    feedbacks = [Feedback(**feedback.to_dict()) async for feedback in feedbacks_stream]

    return feedbacks
