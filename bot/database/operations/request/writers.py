from bot.database.main import firebase
from bot.database.models.common import Model
from bot.database.models.request import Request, RequestStatus
from bot.database.operations.request.helpers import create_request_object


async def write_request(
    user_id: str,
    message_id: int,
    model: Model,
    requested: int,
    status=RequestStatus.STARTED,
    details=None,
) -> Request:
    request = await create_request_object(
        user_id,
        message_id,
        model,
        requested,
        status,
        details,
    )
    await firebase.db.collection(Request.COLLECTION_NAME).document(request.id).set(
        request.to_dict()
    )

    return request
