import inspect
import re
from datetime import datetime, timezone
from typing import List, Dict

from bot.database.models.common import Currency, Quota
from bot.database.models.transaction import ServiceType


class PackageType:
    CHAT_GPT3 = "GPT3"
    CHAT_GPT4 = "GPT4"
    DALL_E = "DALL_E"
    MIDJOURNEY = "MIDJOURNEY"
    FACE_SWAP = "FACE_SWAP"
    MUSIC_GEN = "MUSIC_GEN"
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
    ERROR = 'ERROR'


class Package:
    COLLECTION_NAME = "packages"

    id: str
    user_id: str
    status: PackageStatus
    type: PackageType
    currency: Currency
    amount: float
    quantity: int
    provider_payment_charge_id: str
    until_at: datetime
    created_at: datetime
    edited_at: datetime

    MINIMAL_PRICE = {
        Currency.RUB: 100,
        Currency.USD: 1,
        Currency.EUR: 1,
    }

    def __init__(
        self,
        id: str,
        user_id: str,
        type: PackageType,
        status: PackageStatus,
        currency: Currency,
        amount: float,
        quantity: int,
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
        self.quantity = quantity
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
            PackageType.CHAT_GPT3: '',
            PackageType.CHAT_GPT4: '',
            PackageType.CHAT: '',
            PackageType.DALL_E: '',
            PackageType.MIDJOURNEY: '',
            PackageType.FACE_SWAP: '',
            PackageType.MUSIC_GEN: '',
            PackageType.ACCESS_TO_CATALOG: '',
            PackageType.VOICE_MESSAGES: '',
            PackageType.FAST_MESSAGES: '',
        }

        if currency == Currency.RUB:
            prices[PackageType.CHAT_GPT3] = '1₽'
            prices[PackageType.CHAT_GPT4] = '5₽'
            prices[PackageType.CHAT] = '50₽'
            prices[PackageType.DALL_E] = '5₽'
            prices[PackageType.MIDJOURNEY] = '5₽'
            prices[PackageType.FACE_SWAP] = '5₽'
            prices[PackageType.MUSIC_GEN] = '1₽'
            prices[PackageType.ACCESS_TO_CATALOG] = '50₽'
            prices[PackageType.VOICE_MESSAGES] = '50₽'
            prices[PackageType.FAST_MESSAGES] = '50₽'
        elif currency == Currency.EUR:
            prices[PackageType.CHAT_GPT3] = '0.01€'
            prices[PackageType.CHAT_GPT4] = '0.05€'
            prices[PackageType.CHAT] = '0.5€'
            prices[PackageType.DALL_E] = '0.05€'
            prices[PackageType.MIDJOURNEY] = '0.05€'
            prices[PackageType.FACE_SWAP] = '0.05€'
            prices[PackageType.MUSIC_GEN] = '0.01€'
            prices[PackageType.ACCESS_TO_CATALOG] = '0.5€'
            prices[PackageType.VOICE_MESSAGES] = '0.5€'
            prices[PackageType.FAST_MESSAGES] = '0.5€'
        else:
            prices[PackageType.CHAT_GPT3] = '$0.01'
            prices[PackageType.CHAT_GPT4] = '$0.05'
            prices[PackageType.CHAT] = '$0.5'
            prices[PackageType.DALL_E] = '$0.05'
            prices[PackageType.MIDJOURNEY] = '$0.05'
            prices[PackageType.FACE_SWAP] = '$0.05'
            prices[PackageType.MUSIC_GEN] = '$0.01'
            prices[PackageType.ACCESS_TO_CATALOG] = '$0.5'
            prices[PackageType.VOICE_MESSAGES] = '$0.5'
            prices[PackageType.FAST_MESSAGES] = '$0.5'

        return prices

    @staticmethod
    def get_price(currency: Currency, package_type: PackageType, quantity: int):
        prices = Package.get_prices(currency)
        price_raw = prices[package_type]
        price_clear = re.sub(r'[^\d.]', '', price_raw)
        price = float(price_clear) if '.' in price_clear else int(price_clear)

        return int(quantity * price)

    @staticmethod
    def get_translate_name_and_description(localization, package_type: str):
        name = None
        description = None
        if package_type == PackageType.CHAT_GPT3:
            name = localization.GPT3_REQUESTS
            description = localization.GPT3_REQUESTS_DESCRIPTION
        elif package_type == PackageType.CHAT_GPT4:
            name = localization.GPT4_REQUESTS
            description = localization.GPT4_REQUESTS_DESCRIPTION
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
    def is_above_minimal_price(currency: Currency, cart_items: List[Dict]) -> bool:
        total_price = 0.0
        for cart_item in cart_items:
            total_price += Package.get_price(currency, cart_item.get("package_type"), cart_item.get("quantity", 0))

        return total_price >= Package.MINIMAL_PRICE[currency]

    @staticmethod
    def get_service_type_and_update_quota(package_type: str, additional_usage_quota: dict, quantity: int):
        service_type = package_type
        if package_type == PackageType.CHAT_GPT3:
            additional_usage_quota[Quota.CHAT_GPT3] += quantity
            service_type = ServiceType.CHAT_GPT3
        elif package_type == PackageType.CHAT_GPT4:
            additional_usage_quota[Quota.CHAT_GPT4] += quantity
            service_type = ServiceType.CHAT_GPT4
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
