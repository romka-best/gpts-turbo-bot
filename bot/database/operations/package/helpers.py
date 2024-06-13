from datetime import datetime
from typing import Optional

from bot.database.main import firebase
from bot.database.models.common import Currency, PaymentMethod
from bot.database.models.package import Package, PackageType, PackageStatus


async def create_package_object(
    package_id: Optional[str],
    user_id: str,
    type: PackageType,
    status: PackageStatus,
    currency: Currency,
    amount: float,
    income_amount: float,
    quantity: int,
    payment_method: PaymentMethod,
    provider_payment_charge_id: Optional[str],
    until_at: datetime = None,
) -> Package:
    package_ref = firebase.db.collection(Package.COLLECTION_NAME).document(package_id)
    return Package(
        id=package_ref.id,
        user_id=user_id,
        type=type,
        status=status,
        currency=currency,
        amount=amount,
        income_amount=income_amount,
        quantity=quantity,
        payment_method=payment_method,
        provider_payment_charge_id=provider_payment_charge_id,
        until_at=until_at,
    )
