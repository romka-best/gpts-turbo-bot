import re
from datetime import datetime, timedelta, timezone

from bot.database.models.common import Currency, Quota, PaymentMethod


class SubscriptionType:
    FREE = 'FREE'
    STANDARD = 'STANDARD'
    VIP = 'VIP'
    PREMIUM = 'PREMIUM'


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
            Quota.CHAT_GPT4_OMNI_MINI: 100,
            Quota.CHAT_GPT4_TURBO: 0,
            Quota.CHAT_GPT4_OMNI: 0,
            Quota.CLAUDE_3_SONNET: 0,
            Quota.CLAUDE_3_OPUS: 0,
            Quota.DALL_E: 0,
            Quota.MIDJOURNEY: 0,
            Quota.FACE_SWAP: 0,
            Quota.MUSIC_GEN: 0,
            Quota.SUNO: 0,
        },
        SubscriptionType.STANDARD: {
            Quota.CHAT_GPT4_OMNI_MINI: 1000,
            Quota.CHAT_GPT4_TURBO: 10,
            Quota.CHAT_GPT4_OMNI: 25,
            Quota.CLAUDE_3_SONNET: 25,
            Quota.CLAUDE_3_OPUS: 10,
            Quota.DALL_E: 25,
            Quota.MIDJOURNEY: 10,
            Quota.FACE_SWAP: 100,
            Quota.MUSIC_GEN: 300,
            Quota.SUNO: 25,
        },
        SubscriptionType.VIP: {
            Quota.CHAT_GPT4_OMNI_MINI: 2000,
            Quota.CHAT_GPT4_TURBO: 25,
            Quota.CHAT_GPT4_OMNI: 50,
            Quota.CLAUDE_3_SONNET: 50,
            Quota.CLAUDE_3_OPUS: 25,
            Quota.DALL_E: 50,
            Quota.MIDJOURNEY: 25,
            Quota.FACE_SWAP: 250,
            Quota.MUSIC_GEN: 900,
            Quota.SUNO: 50,
        },
        SubscriptionType.PREMIUM: {
            Quota.CHAT_GPT4_OMNI_MINI: 3000,
            Quota.CHAT_GPT4_TURBO: 50,
            Quota.CHAT_GPT4_OMNI: 100,
            Quota.CLAUDE_3_SONNET: 100,
            Quota.CLAUDE_3_OPUS: 50,
            Quota.DALL_E: 100,
            Quota.MIDJOURNEY: 50,
            Quota.FACE_SWAP: 500,
            Quota.MUSIC_GEN: 1800,
            Quota.SUNO: 100,
        }
    }
    ADDITIONAL_QUOTA_LIMITS = {
        SubscriptionType.FREE: {
            Quota.ADDITIONAL_CHATS: 0,
            Quota.ACCESS_TO_CATALOG: False,
            Quota.FAST_MESSAGES: False,
            Quota.VOICE_MESSAGES: False,
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
        }
    }

    @classmethod
    def get_limits(self, subscription_type):
        return self.LIMITS.get(subscription_type, {})


class Subscription:
    COLLECTION_NAME = "subscriptions"

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
        provider_payment_charge_id="",
        provider_auto_payment_charge_id="",
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
            SubscriptionType.STANDARD: '',
            SubscriptionType.VIP: '',
            SubscriptionType.PREMIUM: ''
        }

        if currency == Currency.RUB:
            prices[SubscriptionType.STANDARD] = '299₽'
            prices[SubscriptionType.VIP] = '749₽'
            prices[SubscriptionType.PREMIUM] = '1 999₽'
        elif currency == Currency.USD:
            prices[SubscriptionType.STANDARD] = '$4.99'
            prices[SubscriptionType.VIP] = '$9.99'
            prices[SubscriptionType.PREMIUM] = '$19.99'
        else:
            prices[SubscriptionType.STANDARD] = '250⭐️'
            prices[SubscriptionType.VIP] = '500⭐️'
            prices[SubscriptionType.PREMIUM] = '1000⭐️'

        return prices

    @staticmethod
    def get_emojis():
        return {
            SubscriptionType.FREE: '🆓',
            SubscriptionType.STANDARD: '⭐',
            SubscriptionType.VIP: '🔥',
            SubscriptionType.PREMIUM: '💎'
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
        price_with_discount = round(price_with_period - (price_with_period * (price_discount[subscription_period] / 100.0)), 2)
        if currency == Currency.XTR:
            price_with_discount = int(price_with_discount)

        return ('%f' % price_with_discount).rstrip('0').rstrip('.')
