from datetime import datetime, timezone
from typing import Optional

from aiogram.types import User as TelegramUser

from bot.database.models.common import Model, Currency, Quota, ChatGPTVersion, ClaudeGPTVersion, GeminiGPTVersion
from bot.database.models.subscription import SUBSCRIPTION_FREE_LIMITS
from bot.database.models.user import User, UserSettings
from bot.locales.types import LanguageCode


def create_user_object(
    telegram_user: TelegramUser,
    user_data: dict,
    chat_id: str,
    telegram_chat_id: str,
    stripe_id: str,
    referred_by: Optional[str],
    is_referred_by_user=False,
    quota=Quota.CHAT_GPT4_OMNI_MINI,
    utm=None,
) -> User:
    default_model = Model.CHAT_GPT
    default_settings = User.DEFAULT_SETTINGS
    if quota in [Quota.CHAT_GPT4_OMNI_MINI, Quota.CHAT_GPT4_OMNI, Quota.CHAT_GPT_O_1_MINI, Quota.CHAT_GPT_O_1]:
        default_model = Model.CHAT_GPT
        if quota == Quota.CHAT_GPT4_OMNI_MINI:
            default_settings[default_model][UserSettings.VERSION] = ChatGPTVersion.V4_Omni_Mini
        elif quota == Quota.CHAT_GPT4_OMNI:
            default_settings[default_model][UserSettings.VERSION] = ChatGPTVersion.V4_Omni
        elif quota == Quota.CHAT_GPT_O_1_MINI:
            default_settings[default_model][UserSettings.VERSION] = ChatGPTVersion.V1_O_Mini
        elif quota == Quota.CHAT_GPT_O_1:
            default_settings[default_model][UserSettings.VERSION] = ChatGPTVersion.V1_O
    elif quota in [Quota.CLAUDE_3_HAIKU, Quota.CLAUDE_3_SONNET, Quota.CLAUDE_3_OPUS]:
        default_model = Model.CLAUDE
        if quota == Quota.CLAUDE_3_HAIKU:
            default_settings[default_model][UserSettings.VERSION] = ClaudeGPTVersion.V3_Haiku
        elif quota == Quota.CLAUDE_3_SONNET:
            default_settings[default_model][UserSettings.VERSION] = ClaudeGPTVersion.V3_Sonnet
        elif quota == Quota.CLAUDE_3_OPUS:
            default_settings[default_model][UserSettings.VERSION] = ClaudeGPTVersion.V3_Opus
    elif quota in [Quota.GEMINI_2_FLASH, Quota.GEMINI_1_PRO, Quota.GEMINI_1_ULTRA]:
        default_model = Model.GEMINI
        if quota == Quota.GEMINI_2_FLASH:
            default_settings[default_model][UserSettings.VERSION] = GeminiGPTVersion.V2_Flash
        elif quota == Quota.GEMINI_1_PRO:
            default_settings[default_model][UserSettings.VERSION] = GeminiGPTVersion.V1_Pro
        elif quota == Quota.GEMINI_1_ULTRA:
            default_settings[default_model][UserSettings.VERSION] = GeminiGPTVersion.V1_Ultra
    elif quota == Quota.EIGHTIFY:
        default_model = Model.EIGHTIFY
    elif quota == Quota.DALL_E:
        default_model = Model.DALL_E
    elif quota == Quota.MIDJOURNEY:
        default_model = Model.MIDJOURNEY
    elif quota == Quota.STABLE_DIFFUSION:
        default_model = Model.STABLE_DIFFUSION
    elif quota == Quota.FLUX:
        default_model = Model.FLUX
    elif quota == Quota.FACE_SWAP:
        default_model = Model.FACE_SWAP
    elif quota == Quota.PHOTOSHOP_AI:
        default_model = Model.PHOTOSHOP_AI
    elif quota == Quota.MUSIC_GEN:
        default_model = Model.MUSIC_GEN
    elif quota == Quota.SUNO:
        default_model = Model.SUNO
    elif quota == Quota.RUNWAY:
        default_model = Model.RUNWAY

    interface_language_code = LanguageCode.EN
    if telegram_user.language_code == LanguageCode.RU:
        interface_language_code = LanguageCode.RU
    elif telegram_user.language_code == LanguageCode.ES:
        interface_language_code = LanguageCode.ES
    elif telegram_user.language_code == LanguageCode.HI:
        interface_language_code = LanguageCode.HI

    return User(
        id=str(telegram_user.id),
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name or '',
        username=telegram_user.username,
        current_chat_id=chat_id,
        telegram_chat_id=telegram_chat_id,
        stripe_id=stripe_id,
        language_code=telegram_user.language_code,
        interface_language_code=user_data.get(
            'interface_language_code',
            interface_language_code,
        ),
        is_premium=telegram_user.is_premium or False,
        is_blocked=False,
        is_banned=False,
        current_model=user_data.get('current_model', default_model),
        currency=user_data.get(
            'currency',
            Currency.RUB if telegram_user.language_code == LanguageCode.RU else Currency.USD
        ),
        balance=user_data.get('balance', 25.00 if is_referred_by_user else 0),
        subscription_id=user_data.get('subscription_id', ''),
        last_subscription_limit_update=user_data.get('last_subscription_limit_update', datetime.now(timezone.utc)),
        daily_limits=user_data.get('daily_limits', SUBSCRIPTION_FREE_LIMITS),
        additional_usage_quota=user_data.get('additional_usage_quota', User.DEFAULT_ADDITIONAL_USAGE_QUOTA),
        settings=user_data.get('settings', default_settings),
        referred_by=user_data.get('referred_by', referred_by),
        utm=utm,
        created_at=user_data.get('created_at', None),
        edited_at=user_data.get('edited_at', None),
    )
