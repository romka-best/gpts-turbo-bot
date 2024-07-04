from datetime import datetime, timezone
from typing import List, Dict

from bot.database.models.package import PackageType

from pydantic import BaseModel, Field


class CartItem(BaseModel):
    package_type: PackageType
    quantity: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    edited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return self.model_dump()


class Cart:
    COLLECTION_NAME = "carts"

    id: str
    user_id: str
    items: List[Dict]
    created_at: datetime
    edited_at: datetime

    def __init__(
        self,
        id: str,
        user_id: str,
        items: List[Dict],
        created_at=None,
        edited_at=None,
    ):
        self.id = id
        self.user_id = user_id
        self.items = items

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
