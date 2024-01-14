from datetime import datetime, timezone
from typing import Dict


class Role:
    id: str
    name: str
    translated_names: Dict
    translated_descriptions: Dict
    translated_instructions: Dict
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 name: str,
                 translated_names: Dict,
                 translated_descriptions: Dict,
                 translated_instructions: Dict,
                 created_at=None,
                 edited_at=None):
        self.id = id
        self.name = name
        self.translated_names = translated_names
        self.translated_descriptions = translated_descriptions
        self.translated_instructions = translated_instructions

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
