from datetime import datetime, timezone

from bot.database.models.common import Currency, Model, Quota
from bot.database.models.subscription import SubscriptionType, SubscriptionLimit


class UserSettings:
    SHOW_NAME_OF_THE_CHAT = 'show_name_of_the_chat'
    SHOW_USAGE_QUOTA = 'show_usage_quota'
    TURN_ON_VOICE_MESSAGES = 'turn_on_voice_messages'


class UserGender:
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    UNSPECIFIED = 'UNSPECIFIED'


class User:
    id: str
    first_name: str
    last_name: str
    username: str
    current_chat_id: str
    telegram_chat_id: str
    language_code: str
    gender: UserGender
    is_premium: bool
    is_blocked: bool
    current_model: str
    currency: Currency
    subscription_type: SubscriptionType
    last_subscription_limit_update: datetime
    monthly_limits: dict
    additional_usage_quota: dict
    settings: dict
    created_at: datetime
    edited_at: datetime

    DEFAULT_ADDITIONAL_USAGE_QUOTA = {
        Quota.GPT3: 0,
        Quota.GPT4: 0,
        Quota.ADDITIONAL_CHATS: 0,
        Quota.DALLE3: 0,
        Quota.FACE_SWAP: 0,
        Quota.FAST_MESSAGES: False,
        Quota.VOICE_MESSAGES: False,
        Quota.ACCESS_TO_CATALOG: False,
    }

    DEFAULT_SETTINGS = {
        UserSettings.SHOW_NAME_OF_THE_CHAT: False,
        UserSettings.SHOW_USAGE_QUOTA: True,
        UserSettings.TURN_ON_VOICE_MESSAGES: False,
    }

    def __init__(self,
                 id: str,
                 first_name: str,
                 last_name: str,
                 username: str,
                 current_chat_id: str,
                 telegram_chat_id: str,
                 gender=UserGender.UNSPECIFIED,
                 language_code="en",
                 is_premium=False,
                 is_blocked=False,
                 current_model=Model.GPT3,
                 currency=Currency.RUB,
                 subscription_type=SubscriptionType.FREE,
                 last_subscription_limit_update=None,
                 monthly_limits=None,
                 additional_usage_quota=None,
                 settings=None,
                 created_at=None,
                 edited_at=None):
        self.id = str(id)
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.gender = gender
        self.language_code = language_code
        self.is_premium = is_premium
        self.is_blocked = is_blocked
        self.current_model = current_model
        self.currency = currency
        self.subscription_type = subscription_type
        self.current_chat_id = str(current_chat_id)
        self.telegram_chat_id = str(telegram_chat_id)
        self.monthly_limits = monthly_limits if monthly_limits is not None \
            else SubscriptionLimit
        self.additional_usage_quota = additional_usage_quota if additional_usage_quota is not None \
            else self.DEFAULT_ADDITIONAL_USAGE_QUOTA
        self.settings = settings if settings is not None else self.DEFAULT_SETTINGS

        current_time = datetime.now(timezone.utc)
        self.last_subscription_limit_update = last_subscription_limit_update \
            if last_subscription_limit_update is not None else current_time
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)
