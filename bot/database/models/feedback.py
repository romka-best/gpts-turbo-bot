from datetime import datetime, timezone


class Feedback:
    id: str
    user_id: str
    content: str
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 user_id: str,
                 content: str,
                 created_at=None,
                 edited_at=None):
        self.id = id
        self.user_id = user_id
        self.content = content

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
