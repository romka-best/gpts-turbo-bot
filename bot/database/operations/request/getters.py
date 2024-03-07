from typing import Optional, List

from google.cloud.firestore_v1 import FieldFilter

from bot.database.main import firebase
from bot.database.models.common import Model
from bot.database.models.request import Request, RequestStatus


async def get_request(request_id: str) -> Optional[Request]:
    request_ref = firebase.db.collection(Request.COLLECTION_NAME).document(str(request_id))
    request = await request_ref.get()

    if request.exists:
        return Request(**request.to_dict())


async def get_started_requests_by_user_id_and_model(user_id: str, model: Model) -> List[Request]:
    requests_stream = firebase.db.collection(Request.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
        .where(filter=FieldFilter("status", "==", RequestStatus.STARTED)) \
        .where(filter=FieldFilter("model", "==", model)) \
        .stream()

    requests = [Request(**request.to_dict()) async for request in requests_stream]

    return requests
