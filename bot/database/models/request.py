from datetime import datetime, timezone

from bot.database.models.common import Model


class RequestStatus:
    STARTED = 'STARTED'
    FINISHED = 'FINISHED'


class Request:
    COLLECTION_NAME = 'requests'

    id: str
    user_id: str
    message_id: int
    model: Model
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
        model: Model,
        requested: int,
        status=RequestStatus.STARTED,
        details=None,
        created_at=None,
        edited_at=None,
    ):
        self.id = id
        self.user_id = user_id
        self.message_id = message_id
        self.model = model
        self.requested = requested
        self.status = status
        self.details = details if details is not None else {}

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
