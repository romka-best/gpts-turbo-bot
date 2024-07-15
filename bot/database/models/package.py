import inspect
import re
from datetime import datetime, timezone

from bot.database.models.common import Currency, Quota, PaymentMethod
from bot.database.models.transaction import ServiceType


class PackageType:
    CHAT_GPT3_TURBO = "GPT3"
    CHAT_GPT4_TURBO = "GPT4"
    CHAT_GPT4_OMNI = "GPT4_OMNI"
    CLAUDE_3_SONNET = "CLAUDE_3_SONNET"
    CLAUDE_3_OPUS = "CLAUDE_3_OPUS"
    DALL_E = "DALL_E"
    MIDJOURNEY = "MIDJOURNEY"
    FACE_SWAP = "FACE_SWAP"
    MUSIC_GEN = "MUSIC_GEN"
    SUNO = "SUNO"
    CHAT = "CHAT"
    ACCESS_TO_CATALOG = "ACCESS_TO_CATALOG"
    VOICE_MESSAGES = "VOICE_MESSAGES"
    FAST_MESSAGES = "FAST_MESSAGES"

    @staticmethod
    def get_class_attributes_in_order():
        source_lines = inspect.getsourcelines(PackageType)[0]
        attributes = []
        for line in source_lines:
            line = line.strip()
            if line.startswith('def ') or line.startswith('@'):
                break
            if '=' in line:
                attribute = line.split('=')[0].strip()
                attributes.append(attribute)
        return [getattr(PackageType, attr) for attr in attributes]


class PackageStatus:
    SUCCESS = 'SUCCESS'
    WAITING = 'WAITING'
    CANCELED = 'CANCELED'
    DECLINED = 'DECLINED'
    ERROR = 'ERROR'


class Package:
    COLLECTION_NAME = "packages"

    id: str
    user_id: str
    status: PackageStatus
    type: PackageType
    currency: Currency
    amount: float
    income_amount: float
    quantity: int
    payment_method: PaymentMethod
    provider_payment_charge_id: str
    until_at: datetime
    created_at: datetime
    edited_at: datetime

    MINIMAL_PRICE = {
        Currency.RUB: 100,
        Currency.USD: 1,
        Currency.XTR: 100,
    }

    def __init__(
        self,
        id: str,
        user_id: str,
        type: PackageType,
        status: PackageStatus,
        currency: Currency,
        amount: float,
        income_amount=0.00,
        quantity=1,
        payment_method=PaymentMethod.YOOKASSA,
        provider_payment_charge_id="",
        until_at=None,
        created_at=None,
        edited_at=None,
    ):
        self.id = id
        self.user_id = user_id
        self.type = type
        self.status = status
        self.currency = currency
        self.amount = amount
        self.income_amount = income_amount
        self.quantity = quantity
        self.payment_method = payment_method
        self.provider_payment_charge_id = provider_payment_charge_id
        self.until_at = until_at

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return vars(self)

    @staticmethod
    def get_prices(currency: Currency):
        prices = {
            PackageType.CHAT_GPT3_TURBO: '',
            PackageType.CHAT_GPT4_TURBO: '',
            PackageType.CHAT_GPT4_OMNI: '',
            PackageType.CLAUDE_3_SONNET: '',
            PackageType.CLAUDE_3_OPUS: '',
            PackageType.CHAT: '',
            PackageType.DALL_E: '',
            PackageType.MIDJOURNEY: '',
            PackageType.FACE_SWAP: '',
            PackageType.MUSIC_GEN: '',
            PackageType.SUNO: '',
            PackageType.ACCESS_TO_CATALOG: '',
            PackageType.VOICE_MESSAGES: '',
            PackageType.FAST_MESSAGES: '',
        }

        if currency == Currency.RUB:
            prices[PackageType.CHAT_GPT3_TURBO] = '1₽'
            prices[PackageType.CHAT_GPT4_TURBO] = '5₽'
            prices[PackageType.CHAT_GPT4_OMNI] = '2.5₽'
            prices[PackageType.CLAUDE_3_SONNET] = '2.5₽'
            prices[PackageType.CLAUDE_3_OPUS] = '5₽'
            prices[PackageType.DALL_E] = '5₽'
            prices[PackageType.MIDJOURNEY] = '10₽'
            prices[PackageType.FACE_SWAP] = '5₽'
            prices[PackageType.MUSIC_GEN] = '1₽'
            prices[PackageType.SUNO] = '5₽'
            prices[PackageType.CHAT] = '25₽'
            prices[PackageType.ACCESS_TO_CATALOG] = '50₽'
            prices[PackageType.VOICE_MESSAGES] = '50₽'
            prices[PackageType.FAST_MESSAGES] = '50₽'
        elif currency == Currency.USD:
            prices[PackageType.CHAT_GPT3_TURBO] = '$0.01'
            prices[PackageType.CHAT_GPT4_TURBO] = '$0.05'
            prices[PackageType.CHAT_GPT4_OMNI] = '$0.025'
            prices[PackageType.CLAUDE_3_SONNET] = '$0.025'
            prices[PackageType.CLAUDE_3_OPUS] = '$0.05'
            prices[PackageType.DALL_E] = '$0.05'
            prices[PackageType.MIDJOURNEY] = '$0.1'
            prices[PackageType.FACE_SWAP] = '$0.05'
            prices[PackageType.MUSIC_GEN] = '$0.01'
            prices[PackageType.SUNO] = '$0.05'
            prices[PackageType.CHAT] = '$0.25'
            prices[PackageType.ACCESS_TO_CATALOG] = '$0.5'
            prices[PackageType.VOICE_MESSAGES] = '$0.5'
            prices[PackageType.FAST_MESSAGES] = '$0.5'
        else:
            prices[PackageType.CHAT_GPT3_TURBO] = '1⭐️'
            prices[PackageType.CHAT_GPT4_TURBO] = '5⭐️'
            prices[PackageType.CHAT_GPT4_OMNI] = '2.5⭐️'
            prices[PackageType.CLAUDE_3_SONNET] = '2.5⭐️'
            prices[PackageType.CLAUDE_3_OPUS] = '5⭐️'
            prices[PackageType.DALL_E] = '5⭐️'
            prices[PackageType.MIDJOURNEY] = '10⭐️'
            prices[PackageType.FACE_SWAP] = '5⭐️'
            prices[PackageType.MUSIC_GEN] = '1⭐️'
            prices[PackageType.SUNO] = '5⭐️'
            prices[PackageType.CHAT] = '25⭐️'
            prices[PackageType.ACCESS_TO_CATALOG] = '50⭐️'
            prices[PackageType.VOICE_MESSAGES] = '50⭐️'
            prices[PackageType.FAST_MESSAGES] = '50⭐️'

        return prices

    @staticmethod
    def get_price(
        currency: Currency,
        package_type: PackageType,
        quantity: int,
        user_discount: int,
    ):
        prices = Package.get_prices(currency)
        price_raw = prices[package_type]
        price_clear = re.sub(r'[^\d.]', '', price_raw)
        price = float(price_clear) if '.' in price_clear else int(price_clear)

        price_with_discount = round(price * quantity - (price * quantity * (user_discount / 100.0)), 2)

        return price_with_discount

    @staticmethod
    def get_translate_name_and_description(localization, package_type: str):
        name = None
        description = None
        if package_type == PackageType.CHAT_GPT3_TURBO:
            name = localization.GPT3_REQUESTS
            description = localization.GPT3_REQUESTS_DESCRIPTION
        elif package_type == PackageType.CHAT_GPT4_TURBO:
            name = localization.GPT4_REQUESTS
            description = localization.GPT4_REQUESTS_DESCRIPTION
        elif package_type == PackageType.CHAT_GPT4_OMNI:
            name = localization.GPT4_OMNI_REQUESTS
            description = localization.GPT4_OMNI_REQUESTS_DESCRIPTION
        elif package_type == PackageType.CLAUDE_3_SONNET:
            name = localization.CLAUDE_3_SONNET_REQUESTS
            description = localization.CLAUDE_3_SONNET_REQUESTS_DESCRIPTION
        elif package_type == PackageType.CLAUDE_3_OPUS:
            name = localization.CLAUDE_3_OPUS_REQUESTS
            description = localization.CLAUDE_3_OPUS_REQUESTS_DESCRIPTION
        elif package_type == PackageType.DALL_E:
            name = localization.DALL_E_REQUESTS
            description = localization.DALL_E_REQUESTS_DESCRIPTION
        elif package_type == PackageType.MIDJOURNEY:
            name = localization.MIDJOURNEY_REQUESTS
            description = localization.MIDJOURNEY_REQUESTS_DESCRIPTION
        elif package_type == PackageType.FACE_SWAP:
            name = localization.FACE_SWAP_REQUESTS
            description = localization.FACE_SWAP_REQUESTS_DESCRIPTION
        elif package_type == PackageType.MUSIC_GEN:
            name = localization.MUSIC_GEN_REQUESTS
            description = localization.MUSIC_GEN_REQUESTS_DESCRIPTION
        elif package_type == PackageType.SUNO:
            name = localization.SUNO_REQUESTS
            description = localization.SUNO_REQUESTS_DESCRIPTION
        elif package_type == PackageType.CHAT:
            name = localization.THEMATIC_CHATS
            description = localization.THEMATIC_CHATS_DESCRIPTION
        elif package_type == PackageType.ACCESS_TO_CATALOG:
            name = localization.ACCESS_TO_CATALOG
            description = localization.ACCESS_TO_CATALOG_DESCRIPTION
        elif package_type == PackageType.VOICE_MESSAGES:
            name = localization.ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES
            description = localization.ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION
        elif package_type == PackageType.FAST_MESSAGES:
            name = localization.FAST_ANSWERS
            description = localization.FAST_ANSWERS_DESCRIPTION

        return {
            "name": name,
            "description": description,
        }

    @staticmethod
    def get_service_type_and_update_quota(package_type: str, additional_usage_quota: dict, quantity: int):
        service_type = package_type
        if package_type == PackageType.CHAT_GPT3_TURBO:
            additional_usage_quota[Quota.CHAT_GPT3_TURBO] += quantity
            service_type = ServiceType.CHAT_GPT3_TURBO
        elif package_type == PackageType.CHAT_GPT4_TURBO:
            additional_usage_quota[Quota.CHAT_GPT4_TURBO] += quantity
            service_type = ServiceType.CHAT_GPT4_TURBO
        elif package_type == PackageType.CHAT_GPT4_OMNI:
            additional_usage_quota[Quota.CHAT_GPT4_OMNI] += quantity
            service_type = ServiceType.CHAT_GPT4_OMNI
        elif package_type == PackageType.CLAUDE_3_SONNET:
            additional_usage_quota[Quota.CLAUDE_3_SONNET] += quantity
            service_type = ServiceType.CLAUDE_3_SONNET
        elif package_type == PackageType.CLAUDE_3_OPUS:
            additional_usage_quota[Quota.CLAUDE_3_OPUS] += quantity
            service_type = ServiceType.CLAUDE_3_OPUS
        elif package_type == PackageType.DALL_E:
            additional_usage_quota[Quota.DALL_E] += quantity
            service_type = ServiceType.DALL_E
        elif package_type == PackageType.MIDJOURNEY:
            additional_usage_quota[Quota.MIDJOURNEY] += quantity
            service_type = ServiceType.MIDJOURNEY
        elif package_type == PackageType.FACE_SWAP:
            additional_usage_quota[Quota.FACE_SWAP] += quantity
            service_type = ServiceType.FACE_SWAP
        elif package_type == PackageType.MUSIC_GEN:
            additional_usage_quota[Quota.MUSIC_GEN] += quantity
            service_type = ServiceType.MUSIC_GEN
        elif package_type == PackageType.SUNO:
            additional_usage_quota[Quota.SUNO] += quantity
            service_type = ServiceType.SUNO
        elif package_type == PackageType.CHAT:
            additional_usage_quota[Quota.ADDITIONAL_CHATS] += quantity
            service_type = ServiceType.ADDITIONAL_CHATS
        elif package_type == PackageType.FAST_MESSAGES:
            additional_usage_quota[Quota.FAST_MESSAGES] = True
            service_type = ServiceType.FAST_MESSAGES
        elif package_type == PackageType.ACCESS_TO_CATALOG:
            additional_usage_quota[Quota.ACCESS_TO_CATALOG] = True
            service_type = ServiceType.ACCESS_TO_CATALOG
        elif package_type == PackageType.VOICE_MESSAGES:
            additional_usage_quota[Quota.VOICE_MESSAGES] = True
            service_type = ServiceType.VOICE_MESSAGES

        return service_type, additional_usage_quota
