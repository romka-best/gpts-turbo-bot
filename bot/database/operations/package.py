from datetime import datetime, timezone
from typing import Optional, Dict, List
from google.cloud.firestore import Query

from bot.database.main import firebase
from bot.database.models.common import Currency
from bot.database.models.package import Package, PackageType, PackageStatus


async def get_package(package_id: str) -> Optional[Package]:
    package_ref = firebase.db.collection("packages").document(str(package_id))
    package = await package_ref.get()

    if package.exists:
        package_dict = package.to_dict()
        return Package(
            id=package_dict.get('id'),
            user_id=package_dict.get('user_id'),
            type=package_dict.get('type'),
            status=package_dict.get('status'),
            currency=package_dict.get('currency'),
            amount=package_dict.get('amount'),
            quantity=package_dict.get('quantity'),
            provider_payment_charge_id=package_dict.get('provider_payment_charge_id'),
            until_at=package_dict.get('until_at'),
            created_at=package_dict.get('created_at'),
            edited_at=package_dict.get('edited_at'),
        )


async def get_last_package_by_user_id(user_id: str) -> Optional[Package]:
    package_stream = firebase.db.collection("packages") \
        .where("user_id", "==", user_id) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .limit(1) \
        .stream()

    async for package in package_stream:
        package_dict = package.to_dict()
        return Package(
            id=package_dict.get('id'),
            user_id=package_dict.get('user_id'),
            type=package_dict.get('type'),
            status=package_dict.get('status'),
            currency=package_dict.get('currency'),
            amount=package_dict.get('amount'),
            quantity=package_dict.get('quantity'),
            provider_payment_charge_id=package_dict.get('provider_payment_charge_id'),
            until_at=package_dict.get('until_at'),
            created_at=package_dict.get('created_at'),
            edited_at=package_dict.get('edited_at'),
        )


async def get_packages_by_user_id(user_id: str) -> List[Package]:
    packages_query = firebase.db.collection("packages").where("user_id", "==", user_id)
    packages = [
        Package(
            id=package.to_dict().get('id'),
            user_id=package.to_dict().get('user_id'),
            type=package.to_dict().get('type'),
            status=package.to_dict().get('status'),
            currency=package.to_dict().get('currency'),
            amount=package.to_dict().get('amount'),
            quantity=package.to_dict().get('quantity'),
            provider_payment_charge_id=package.to_dict().get('provider_payment_charge_id'),
            until_at=package.to_dict().get('until_at'),
            created_at=package.to_dict().get('created_at'),
            edited_at=package.to_dict().get('edited_at'),
        ) async for package in packages_query.stream()
    ]

    return packages


async def create_package_object(user_id: str,
                                type: PackageType,
                                status: PackageStatus,
                                currency: Currency,
                                amount: float,
                                quantity: int,
                                until_at: datetime = None) -> Package:
    package_ref = firebase.db.collection('packages').document()
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


async def write_package(user_id: str,
                        type: PackageType,
                        status: PackageStatus,
                        currency: Currency,
                        amount: float,
                        quantity: int,
                        until_at: datetime = None) -> Package:
    package = await create_package_object(user_id, type, status, currency, amount, quantity, until_at)
    await firebase.db.collection('packages').document(package.id).set(package.to_dict())

    return package


async def update_package(package_id: str, data: Dict):
    package_ref = firebase.db.collection('packages').document(package_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await package_ref.update(data)


async def update_package_in_transaction(transaction, package_id: str, data: Dict):
    data['edited_at'] = datetime.now(timezone.utc)

    transaction.update(firebase.db.collection('packages').document(package_id), data)
