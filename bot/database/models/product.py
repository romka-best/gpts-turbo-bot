from datetime import datetime, timezone
from enum import Enum
from typing import Optional, ClassVar, Union

from pydantic import BaseModel, Field

from bot.database.models.common import Currency, ModelType
from bot.database.models.subscription import SubscriptionType, SubscriptionPeriod


class ProductType(str, Enum):
    SUBSCRIPTION = 'SUBSCRIPTION'
    PACKAGE = 'PACKAGE'


class ProductCategory(str, Enum):
    MONTHLY = SubscriptionType.MONTHLY
    YEARLY = SubscriptionType.YEARLY
    TEXT = ModelType.TEXT
    IMAGE = ModelType.IMAGE
    MUSIC = ModelType.MUSIC
    VIDEO = ModelType.VIDEO
    OTHER = 'OTHER'


class Product(BaseModel):
    COLLECTION_NAME: ClassVar[str] = 'products'

    id: str
    stripe_id: str
    is_active: bool
    type: ProductType
    category: ProductCategory
    names: dict
    descriptions: dict
    prices: dict
    photos: Optional[dict] = None
    order: int = -1
    discount: int = 0
    details: Optional[dict] = {}
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    edited_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return vars(self)

    @staticmethod
    def get_discount_price(
        type: ProductType,
        quantity: int,
        price: Union[int, float],
        currency: Currency,
        discount: int,
        subscription_period: Optional[SubscriptionPeriod] = None,
    ) -> str:
        if type == ProductType.SUBSCRIPTION:
            price_discount = {
                SubscriptionPeriod.MONTH1: discount if discount > 0 else 0,
                SubscriptionPeriod.MONTHS3: discount if discount > 5 else 5,
                SubscriptionPeriod.MONTHS6: discount if discount > 10 else 10,
                SubscriptionPeriod.MONTHS12: discount if discount > 20 else 20,
            }
            price_period = {
                SubscriptionPeriod.MONTH1: 1,
                SubscriptionPeriod.MONTHS3: 3,
                SubscriptionPeriod.MONTHS6: 6,
                SubscriptionPeriod.MONTHS12: 12,
            }

            price_with_period = price * price_period[subscription_period]
            price_with_discount = round(
                price_with_period - (price_with_period * (price_discount[subscription_period] / 100.0)),
                2,
            )
            if currency == Currency.XTR:
                price_with_discount = int(price_with_discount)
        else:
            price_with_discount = round(
                price * quantity - (price * quantity * (discount / 100.0)),
                2,
            )

        return ('%f' % price_with_discount).rstrip('0').rstrip('.')
