from datetime import datetime, timezone
from typing import Optional, Dict, List
from google.cloud.firestore import Query

from bot.database.main import db
from bot.database.models.common import Currency
from bot.database.models.package import Package, PackageType, PackageStatus


async def get_package(package_id: str) -> Optional[Package]:
    package_ref = db.collection("packages").document(str(package_id))
    package = await package_ref.get()

    if package.exists:
        return Package(**package.to_dict())


async def get_last_package_by_user_id(user_id: str) -> Optional[Package]:
    package_stream = db.collection("packages") \
        .where("user_id", "==", user_id) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .limit(1) \
        .stream()

    async for doc in package_stream:
        return Package(**doc.to_dict())


async def get_packages_by_user_id(user_id: str) -> List[Package]:
    packages_query = db.collection("packages").where("user_id", "==", user_id)
    packages = [Package(**package.to_dict()) async for package in packages_query.stream()]

    return packages


async def create_package_object(user_id: str,
                                type: PackageType,
                                status: PackageStatus,
                                currency: Currency,
                                amount: float,
                                quantity: int) -> Package:
    package_ref = db.collection('packages').document()
    return Package(
        id=package_ref.id,
        user_id=user_id,
        type=type,
        status=status,
        currency=currency,
        amount=amount,
        quantity=quantity
    )


async def write_package(user_id: str,
                        type: PackageType,
                        status: PackageStatus,
                        currency: Currency,
                        amount: float,
                        quantity: int) -> Package:
    package = await create_package_object(user_id, type, status, currency, amount, quantity)
    await db.collection('packages').document(package.id).set(package.to_dict())

    return package


async def update_package(package_id: str, data: Dict):
    package_ref = db.collection('packages').document(package_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await package_ref.update(data)


async def update_package_in_transaction(transaction, package_id: str, data: Dict):
    data['edited_at'] = datetime.now(timezone.utc)

    transaction.update(db.collection('packages').document(package_id), data)
