from bot.database.main import firebase
from bot.database.models.request import Request, RequestStatus


async def create_request_object(
    user_id: str,
    message_id: int,
    product_id: str,
    requested: int,
    status=RequestStatus.STARTED,
    details=None,
) -> Request:
    request_ref = firebase.db.collection(Request.COLLECTION_NAME).document()
    return Request(
        id=request_ref.id,
        user_id=user_id,
        message_id=message_id,
        product_id=product_id,
        requested=requested,
        status=status,
        details=details,
    )
