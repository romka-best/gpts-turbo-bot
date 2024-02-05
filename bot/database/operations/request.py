from datetime import datetime, timezone
from typing import Optional, Dict, List

from bot.database.main import firebase
from bot.database.models.common import Model
from bot.database.models.request import Request, RequestStatus


async def get_request(request_id: str) -> Optional[Request]:
    request_ref = firebase.db.collection("requests").document(str(request_id))
    request = await request_ref.get()

    if request.exists:
        return Request(**request.to_dict())


async def get_started_requests_by_user_id_and_model(user_id: str, model: Model) -> List[Request]:
    requests_stream = firebase.db.collection("requests") \
        .where("user_id", "==", user_id) \
        .where("status", "==", RequestStatus.STARTED) \
        .where("model", "==", model) \
        .stream()

    requests = [Request(**request.to_dict()) async for request in requests_stream]

    return requests


async def create_request_object(user_id: str,
                                message_id: int,
                                model: Model,
                                requested: int,
                                status=RequestStatus.STARTED,
                                details=None) -> Request:
    request_ref = firebase.db.collection('requests').document()
    return Request(
        id=request_ref.id,
        user_id=user_id,
        message_id=message_id,
        model=model,
        requested=requested,
        status=status,
        details=details,
    )


async def write_request(user_id: str,
                        message_id: int,
                        model: Model,
                        requested: int,
                        status=RequestStatus.STARTED,
                        details=None) -> Request:
    request = await create_request_object(user_id,
                                          message_id,
                                          model,
                                          requested,
                                          status,
                                          details)
    await firebase.db.collection('requests').document(request.id).set(
        request.to_dict()
    )

    return request


async def update_request(request_id: str, data: Dict):
    request_ref = firebase.db.collection('requests').document(request_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await request_ref.update(data)
