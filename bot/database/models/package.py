from datetime import datetime, timezone

from bot.database.models.common import Currency, PaymentMethod


# TODO DELETE AFTER MIGRATION
class PackageType:
    CHAT_GPT4_OMNI_MINI = 'GPT4_OMNI_MINI'
    CHAT_GPT4_OMNI = 'GPT4_OMNI'
    CHAT_GPT_O_1_MINI = 'CHAT_GPT_O_1_MINI'
    CHAT_GPT_O_1_PREVIEW = 'CHAT_GPT_O_1_PREVIEW'
    CLAUDE_3_HAIKU = 'CLAUDE_3_HAIKU'
    CLAUDE_3_SONNET = 'CLAUDE_3_SONNET'
    CLAUDE_3_OPUS = 'CLAUDE_3_OPUS'
    GEMINI_1_FLASH = 'GEMINI_1_FLASH'
    GEMINI_1_PRO = 'GEMINI_1_PRO'
    GEMINI_1_ULTRA = 'GEMINI_1_ULTRA'
    DALL_E = 'DALL_E'
    MIDJOURNEY = 'MIDJOURNEY'
    STABLE_DIFFUSION = 'STABLE_DIFFUSION'
    FLUX = 'FLUX'
    FACE_SWAP = 'FACE_SWAP'
    PHOTOSHOP_AI = 'PHOTOSHOP_AI'
    MUSIC_GEN = 'MUSIC_GEN'
    SUNO = 'SUNO'
    CHAT = 'CHAT'
    ACCESS_TO_CATALOG = 'ACCESS_TO_CATALOG'
    VOICE_MESSAGES = 'VOICE_MESSAGES'
    FAST_MESSAGES = 'FAST_MESSAGES'


class PackageStatus:
    SUCCESS = 'SUCCESS'
    WAITING = 'WAITING'
    CANCELED = 'CANCELED'
    DECLINED = 'DECLINED'
    ERROR = 'ERROR'


class Package:
    COLLECTION_NAME = 'packages'

    id: str
    user_id: str
    status: PackageStatus
    product_id: str
    currency: Currency
    amount: float
    income_amount: float
    quantity: int
    payment_method: PaymentMethod
    provider_payment_charge_id: str
    until_at: datetime
    created_at: datetime
    edited_at: datetime

    def __init__(
        self,
        id: str,
        user_id: str,
        status: PackageStatus,
        currency: Currency,
        amount: float,
        product_id='',
        income_amount=0.00,
        quantity=1,
        payment_method=PaymentMethod.YOOKASSA,
        provider_payment_charge_id='',
        until_at=None,
        created_at=None,
        edited_at=None,
        **kwargs,
    ):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.status = status
        self.currency = currency
        self.amount = amount
        self.income_amount = income_amount
        self.quantity = quantity
        self.payment_method = payment_method
        self.provider_payment_charge_id = provider_payment_charge_id
        self.product_id = product_id
        self.until_at = until_at

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
