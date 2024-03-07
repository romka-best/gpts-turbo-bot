from datetime import datetime, timezone

from bot.database.models.common import Currency


class TransactionType:
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class ServiceType:
    STANDARD = "STANDARD"
    VIP = "VIP"
    PLATINUM = "PLATINUM"
    GPT3 = "GPT3"
    GPT4 = "GPT4"
    DALLE3 = "DALLE3"
    FACE_SWAP = "FACE_SWAP"
    MUSIC_GEN = "MUSIC_GEN"
    ADDITIONAL_CHATS = "ADDITIONAL_CHATS"
    FAST_MESSAGES = "FAST_MESSAGES"
    VOICE_MESSAGES = "VOICE_MESSAGES"
    ACCESS_TO_CATALOG = "ACCESS_TO_CATALOG"
    SERVER = "SERVER"
    DATABASE = "DATABASE"
    OTHER = "OTHER"


class Transaction:
    COLLECTION_NAME = "transactions"

    id: str
    user_id: str
    type: TransactionType
    service: ServiceType
    amount: float
    currency: Currency
    quantity: int
    details: dict
    created_at: datetime
    edited_at: datetime

    def __init__(
        self,
        id: str,
        user_id: str,
        type: TransactionType,
        service: ServiceType,
        amount: float,
        currency: Currency,
        quantity=1,
        details=None,
        created_at=None,
        edited_at=None,
    ):
        self.id = str(id)
        self.user_id = str(user_id)
        self.type = type
        self.service = service
        self.amount = amount
        self.currency = currency
        self.quantity = quantity
        self.details = {} if details is None else details

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
