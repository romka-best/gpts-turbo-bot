from datetime import datetime, timezone


class Message:
    id: str
    chat_id: str
    sender: str
    sender_id: str
    content: str
    is_in_context: bool
    photo_filename: str
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 chat_id: str,
                 sender: str,
                 sender_id: str,
                 content: str,
                 is_in_context=True,
                 photo_filename=None,
                 created_at=None,
                 edited_at=None):
        self.id = str(id)
        self.chat_id = str(chat_id)
        self.sender = sender
        self.sender_id = str(sender_id)
        self.content = content
        self.is_in_context = is_in_context
        self.photo_filename = photo_filename

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
