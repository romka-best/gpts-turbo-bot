from datetime import datetime

from bot.database.main import firebase
from bot.database.models.common import Currency
from bot.database.models.package import Package, PackageType, PackageStatus


async def create_package_object(
    user_id: str,
    type: PackageType,
    status: PackageStatus,
    currency: Currency,
    amount: float,
    quantity: int,
    until_at: datetime = None,
) -> Package:
    package_ref = firebase.db.collection(Package.COLLECTION_NAME).document()
    return Package(
        id=package_ref.id,
        user_id=user_id,
        type=type,
        status=status,
        currency=currency,
        amount=amount,
        quantity=quantity,
        until_at=until_at,
    )
