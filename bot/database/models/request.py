from datetime import datetime, timezone


class RequestStatus:
    STARTED = 'STARTED'
    FINISHED = 'FINISHED'


class Request:
    COLLECTION_NAME = 'requests'

    id: str
    user_id: str
    message_id: int
    product_id: str
    requested: int
    status: RequestStatus
    details: dict
    created_at: datetime
    edited_at: datetime

    def __init__(
        self,
        id: str,
        user_id: str,
        message_id: int,
        requested: int,
        # TODO MAKE : str
        product_id='',
        status=RequestStatus.STARTED,
        details=None,
        created_at=None,
        edited_at=None,
        **kwargs,
    ):
        self.id = id
        self.user_id = user_id
        self.message_id = message_id
        self.product_id = product_id
        self.requested = requested
        self.status = status
        self.details = details if details is not None else {}

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
