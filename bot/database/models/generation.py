from datetime import datetime, timezone

from bot.database.models.common import Model


class GenerationStatus:
    STARTED = 'STARTED'
    FINISHED = 'FINISHED'


class GenerationReaction:
    NONE = 'NONE'
    LIKED = 'LIKED'
    DISLIKED = 'DISLIKED'


class Generation:
    COLLECTION_NAME = 'generations'

    id: str
    request_id: str
    model: Model
    result: str
    has_error: bool
    status: GenerationStatus
    reaction: GenerationReaction
    seconds: float
    details: dict
    created_at: datetime
    edited_at: datetime

    def __init__(
        self,
        id: str,
        request_id: str,
        model: Model,
        result='',
        has_error=False,
        status=GenerationStatus.STARTED,
        reaction=GenerationReaction.NONE,
        seconds=0.00,
        details=None,
        created_at=None,
        edited_at=None,
    ):
        self.id = id
        self.request_id = request_id
        self.model = model
        self.result = result
        self.has_error = has_error
        self.status = status
        self.reaction = reaction
        self.seconds = seconds
        self.details = details if details is not None else {}

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)

    @staticmethod
    def get_reaction_emojis():
        return {
            GenerationReaction.NONE: '',
            GenerationReaction.LIKED: '👍',
            GenerationReaction.DISLIKED: '👎',
        }
