from datetime import datetime, timezone

from bot.database.models.common import DEFAULT_ROLE


class Chat:
    id: str
    user_id: str
    telegram_chat_id: str
    title: str
    role: str
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 user_id: str,
                 telegram_chat_id: str,
                 title: str,
                 role=None,
                 created_at=None,
                 edited_at=None):
        self.id = str(id)
        self.user_id = user_id
        self.telegram_chat_id = str(telegram_chat_id)
        self.title = title
        self.role = role if role is not None else DEFAULT_ROLE

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
