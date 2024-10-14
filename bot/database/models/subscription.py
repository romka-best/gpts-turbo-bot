import re
from datetime import datetime, timedelta, timezone

from bot.database.models.common import Currency, Quota, PaymentMethod


class SubscriptionType:
    FREE = 'FREE'
    MINI = 'MINI'
    STANDARD = 'STANDARD'
    VIP = 'VIP'
    PREMIUM = 'PREMIUM'
    UNLIMITED = 'UNLIMITED'


class SubscriptionPeriod:
    MONTH1 = 'MONTH_1'
    MONTHS3 = 'MONTHS_3'
    MONTHS6 = 'MONTHS_6'
    MONTHS12 = 'MONTHS_12'


class SubscriptionStatus:
    ACTIVE = 'ACTIVE'
    WAITING = 'WAITING'
    FINISHED = 'FINISHED'
    DECLINED = 'DECLINED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'


class SubscriptionLimit:
    LIMITS = {
        SubscriptionType.FREE: {
            Quota.CHAT_GPT4_OMNI_MINI: 10,
            Quota.CHAT_GPT4_OMNI: 0,
            Quota.CLAUDE_3_HAIKU: 10,
            Quota.CLAUDE_3_SONNET: 0,
            Quota.CLAUDE_3_OPUS: 0,
            Quota.GEMINI_1_FLASH: 10,
            Quota.GEMINI_1_PRO: 0,
            Quota.GEMINI_1_ULTRA: 0,
            Quota.CHAT_GPT_O_1_MINI: 0,
            Quota.CHAT_GPT_O_1_PREVIEW: 0,
            Quota.DALL_E: 1,
            Quota.MIDJOURNEY: 1,
            Quota.STABLE_DIFFUSION: 1,
            Quota.FLUX: 1,
            Quota.FACE_SWAP: 1,
            Quota.PHOTOSHOP_AI: 1,
            Quota.MUSIC_GEN: 0,
            Quota.SUNO: 0,
        },
        SubscriptionType.MINI: {
            Quota.CHAT_GPT4_OMNI_MINI: 20,
            Quota.CHAT_GPT4_OMNI: 5,
            Quota.CLAUDE_3_HAIKU: 20,
            Quota.CLAUDE_3_SONNET: 5,
            Quota.CLAUDE_3_OPUS: 0,
            Quota.GEMINI_1_FLASH: 20,
            Quota.GEMINI_1_PRO: 5,
            Quota.GEMINI_1_ULTRA: 0,
            Quota.CHAT_GPT_O_1_MINI: 5,
            Quota.CHAT_GPT_O_1_PREVIEW: 0,
            Quota.DALL_E: 5,
            Quota.MIDJOURNEY: 5,
            Quota.STABLE_DIFFUSION: 5,
            Quota.FLUX: 5,
            Quota.FACE_SWAP: 5,
            Quota.PHOTOSHOP_AI: 5,
            Quota.MUSIC_GEN: 2,
            Quota.SUNO: 2,
        },
        SubscriptionType.STANDARD: {
            Quota.CHAT_GPT4_OMNI_MINI: 100,
            Quota.CHAT_GPT4_OMNI: 10,
            Quota.CLAUDE_3_HAIKU: 100,
            Quota.CLAUDE_3_SONNET: 10,
            Quota.CLAUDE_3_OPUS: 5,
            Quota.GEMINI_1_FLASH: 100,
            Quota.GEMINI_1_PRO: 10,
            Quota.GEMINI_1_ULTRA: 5,
            Quota.CHAT_GPT_O_1_MINI: 10,
            Quota.CHAT_GPT_O_1_PREVIEW: 5,
            Quota.DALL_E: 10,
            Quota.MIDJOURNEY: 10,
            Quota.STABLE_DIFFUSION: 10,
            Quota.FLUX: 10,
            Quota.FACE_SWAP: 10,
            Quota.PHOTOSHOP_AI: 10,
            Quota.MUSIC_GEN: 5,
            Quota.SUNO: 5,
        },
        SubscriptionType.VIP: {
            Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
            Quota.CHAT_GPT4_OMNI: 25,
            Quota.CLAUDE_3_HAIKU: float('inf'),
            Quota.CLAUDE_3_SONNET: 25,
            Quota.CLAUDE_3_OPUS: 10,
            Quota.GEMINI_1_FLASH: float('inf'),
            Quota.GEMINI_1_PRO: 25,
            Quota.GEMINI_1_ULTRA: 10,
            Quota.CHAT_GPT_O_1_MINI: 25,
            Quota.CHAT_GPT_O_1_PREVIEW: 10,
            Quota.DALL_E: 15,
            Quota.MIDJOURNEY: 15,
            Quota.STABLE_DIFFUSION: 15,
            Quota.FLUX: 15,
            Quota.FACE_SWAP: 15,
            Quota.PHOTOSHOP_AI: 15,
            Quota.MUSIC_GEN: 10,
            Quota.SUNO: 10,
        },
        SubscriptionType.PREMIUM: {
            Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
            Quota.CHAT_GPT4_OMNI: 100,
            Quota.CLAUDE_3_HAIKU: float('inf'),
            Quota.CLAUDE_3_SONNET: 100,
            Quota.CLAUDE_3_OPUS: 20,
            Quota.GEMINI_1_FLASH: float('inf'),
            Quota.GEMINI_1_PRO: 100,
            Quota.GEMINI_1_ULTRA: 20,
            Quota.CHAT_GPT_O_1_MINI: 100,
            Quota.CHAT_GPT_O_1_PREVIEW: 20,
            Quota.DALL_E: 30,
            Quota.MIDJOURNEY: 30,
            Quota.STABLE_DIFFUSION: 30,
            Quota.FLUX: 30,
            Quota.FACE_SWAP: 30,
            Quota.PHOTOSHOP_AI: 30,
            Quota.MUSIC_GEN: 20,
            Quota.SUNO: 20,
        },
        SubscriptionType.UNLIMITED: {
            Quota.CHAT_GPT4_OMNI_MINI: float('inf'),
            Quota.CHAT_GPT4_OMNI: float('inf'),
            Quota.CLAUDE_3_HAIKU: float('inf'),
            Quota.CLAUDE_3_SONNET: float('inf'),
            Quota.CLAUDE_3_OPUS: float('inf'),
            Quota.GEMINI_1_FLASH: float('inf'),
            Quota.GEMINI_1_PRO: float('inf'),
            Quota.GEMINI_1_ULTRA: float('inf'),
            Quota.CHAT_GPT_O_1_MINI: float('inf'),
            Quota.CHAT_GPT_O_1_PREVIEW: float('inf'),
            Quota.DALL_E: float('inf'),
            Quota.MIDJOURNEY: float('inf'),
            Quota.STABLE_DIFFUSION: float('inf'),
            Quota.FLUX: float('inf'),
            Quota.FACE_SWAP: float('inf'),
            Quota.PHOTOSHOP_AI: float('inf'),
            Quota.MUSIC_GEN: float('inf'),
            Quota.SUNO: float('inf'),
        }
    }
    ADDITIONAL_QUOTA_LIMITS = {
        SubscriptionType.FREE: {
            Quota.ADDITIONAL_CHATS: 0,
            Quota.ACCESS_TO_CATALOG: False,
            Quota.FAST_MESSAGES: False,
            Quota.VOICE_MESSAGES: False,
        },
        SubscriptionType.MINI: {
            Quota.ADDITIONAL_CHATS: 1,
            Quota.ACCESS_TO_CATALOG: True,
            Quota.FAST_MESSAGES: True,
            Quota.VOICE_MESSAGES: True,
        },
        SubscriptionType.STANDARD: {
            Quota.ADDITIONAL_CHATS: 4,
            Quota.ACCESS_TO_CATALOG: True,
            Quota.FAST_MESSAGES: True,
            Quota.VOICE_MESSAGES: True,
        },
        SubscriptionType.VIP: {
            Quota.ADDITIONAL_CHATS: 9,
            Quota.ACCESS_TO_CATALOG: True,
            Quota.FAST_MESSAGES: True,
            Quota.VOICE_MESSAGES: True,
        },
        SubscriptionType.PREMIUM: {
            Quota.ADDITIONAL_CHATS: 19,
            Quota.ACCESS_TO_CATALOG: True,
            Quota.FAST_MESSAGES: True,
            Quota.VOICE_MESSAGES: True,
        },
        SubscriptionType.UNLIMITED: {
            Quota.ADDITIONAL_CHATS: 49,
            Quota.ACCESS_TO_CATALOG: True,
            Quota.FAST_MESSAGES: True,
            Quota.VOICE_MESSAGES: True,
        }
    }
    DISCOUNT = {
        SubscriptionType.FREE: 0,
        SubscriptionType.MINI: 10,
        SubscriptionType.STANDARD: 20,
        SubscriptionType.VIP: 30,
        SubscriptionType.PREMIUM: 50,
        SubscriptionType.UNLIMITED: 50,
    }


class Subscription:
    COLLECTION_NAME = 'subscriptions'

    id: str
    user_id: str
    type: SubscriptionType
    period: SubscriptionPeriod
    status: SubscriptionStatus
    currency: Currency
    amount: float
    income_amount: float
    payment_method: PaymentMethod
    provider_payment_charge_id: str
    provider_auto_payment_charge_id: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    edited_at: datetime

    def __init__(
        self,
        id: str,
        user_id: str,
        type: SubscriptionType,
        period: SubscriptionPeriod,
        status: SubscriptionStatus,
        currency: Currency,
        amount: float,
        income_amount=0.00,
        payment_method=PaymentMethod.YOOKASSA,
        provider_payment_charge_id='',
        provider_auto_payment_charge_id='',
        start_date=None,
        end_date=None,
        created_at=None,
        edited_at=None,
    ):
        self.id = str(id)
        self.user_id = str(user_id)
        self.type = type
        self.period = period
        self.status = status
        self.currency = currency
        self.amount = amount
        self.income_amount = income_amount
        self.payment_method = payment_method
        self.provider_payment_charge_id = provider_payment_charge_id
        self.provider_auto_payment_charge_id = provider_auto_payment_charge_id

        self.start_date = start_date if start_date is not None else datetime.now(timezone.utc)
        if not end_date and period == SubscriptionPeriod.MONTH1:
            self.end_date = self.start_date + timedelta(days=30)
        elif not end_date and period == SubscriptionPeriod.MONTHS3:
            self.end_date = self.start_date + timedelta(days=90)
        elif not end_date and period == SubscriptionPeriod.MONTHS6:
            self.end_date = self.start_date + timedelta(days=180)
        elif not end_date and period == SubscriptionPeriod.MONTHS12:
            self.end_date = self.start_date + timedelta(days=365)
        else:
            self.end_date = end_date

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)

    @staticmethod
    def get_prices(currency: Currency):
        prices = {
            SubscriptionType.MINI: '',
            SubscriptionType.STANDARD: '',
            SubscriptionType.VIP: '',
            SubscriptionType.PREMIUM: '',
            SubscriptionType.UNLIMITED: '',
        }

        if currency == Currency.RUB:
            prices[SubscriptionType.MINI] = '199₽'
            prices[SubscriptionType.STANDARD] = '299₽'
            prices[SubscriptionType.VIP] = '749₽'
            prices[SubscriptionType.PREMIUM] = '1 999₽'
            prices[SubscriptionType.UNLIMITED] = '4 999₽'
        elif currency == Currency.USD:
            prices[SubscriptionType.MINI] = '$2.99'
            prices[SubscriptionType.STANDARD] = '$4.99'
            prices[SubscriptionType.VIP] = '$9.99'
            prices[SubscriptionType.PREMIUM] = '$19.99'
            prices[SubscriptionType.UNLIMITED] = '$49.99'
        else:
            prices[SubscriptionType.MINI] = '150⭐️'
            prices[SubscriptionType.STANDARD] = '250⭐️'
            prices[SubscriptionType.VIP] = '500⭐️'
            prices[SubscriptionType.PREMIUM] = '1000⭐️'
            prices[SubscriptionType.UNLIMITED] = '2500⭐️'

        return prices

    @staticmethod
    def get_emojis():
        return {
            SubscriptionType.FREE: '🆓',
            SubscriptionType.MINI: '🍬',
            SubscriptionType.STANDARD: '⭐',
            SubscriptionType.VIP: '🔥',
            SubscriptionType.PREMIUM: '💎',
            SubscriptionType.UNLIMITED: '🚀',
        }

    @staticmethod
    def get_price(
        currency: Currency,
        subscription_type: SubscriptionType,
        subscription_period: SubscriptionPeriod,
        user_discount: int,
    ):
        price_discount = {
            SubscriptionPeriod.MONTH1: user_discount if user_discount > 0 else 0,
            SubscriptionPeriod.MONTHS3: user_discount if user_discount > 5 else 5,
            SubscriptionPeriod.MONTHS6: user_discount if user_discount > 10 else 10,
            SubscriptionPeriod.MONTHS12: user_discount if user_discount > 20 else 20,
        }
        price_period = {
            SubscriptionPeriod.MONTH1: 1,
            SubscriptionPeriod.MONTHS3: 3,
            SubscriptionPeriod.MONTHS6: 6,
            SubscriptionPeriod.MONTHS12: 12,
        }

        prices = Subscription.get_prices(currency)
        price_raw = prices[subscription_type]
        price_clear = re.sub(r'[^\d.]', '', price_raw)
        price = float(price_clear) if '.' in price_clear else int(price_clear)
        price_with_period = price * price_period[subscription_period]
        price_with_discount = round(
            price_with_period - (price_with_period * (price_discount[subscription_period] / 100.0)),
            2
        )
        if currency == Currency.XTR:
            price_with_discount = int(price_with_discount)

        return ('%f' % price_with_discount).rstrip('0').rstrip('.')
