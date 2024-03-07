from datetime import datetime

from bot.database.main import firebase
from bot.database.models.common import Currency
from bot.database.models.package import Package, PackageType, PackageStatus
from bot.database.operations.package.helpers import create_package_object


async def write_package(
    user_id: str,
    type: PackageType,
    status: PackageStatus,
    currency: Currency,
    amount: float,
    quantity: int,
    until_at: datetime = None,
) -> Package:
    package = await create_package_object(user_id, type, status, currency, amount, quantity, until_at)
    await firebase.db.collection(Package.COLLECTION_NAME).document(package.id).set(package.to_dict())

    return package
