from typing import Optional

from bot.database.main import firebase
from bot.database.models.feedback import Feedback


async def get_feedback(feedback_id: str) -> Optional[Feedback]:
    feedback_ref = firebase.db.collection("feedbacks").document(feedback_id)
    feedback = await feedback_ref.get()

    if feedback.exists:
        return Feedback(**feedback.to_dict())


async def create_feedback_object(user_id: str, content: str) -> Feedback:
    feedback_ref = firebase.db.collection('feedbacks').document()

    return Feedback(
        id=feedback_ref.id,
        user_id=user_id,
        content=content
    )


async def write_feedback(user_id: str, content: str) -> Feedback:
    feedback = await create_feedback_object(user_id, content)
    await firebase.db.collection('feedbacks').document(feedback.id).set(feedback.to_dict())

    return feedback
