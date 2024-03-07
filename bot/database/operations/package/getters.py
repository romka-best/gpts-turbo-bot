from typing import Optional, List

from google.cloud.firestore_v1 import FieldFilter, Query

from bot.database.main import firebase
from bot.database.models.package import Package, PackageStatus


async def get_package(package_id: str) -> Optional[Package]:
    package_ref = firebase.db.collection(Package.COLLECTION_NAME).document(str(package_id))
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
    package_stream = firebase.db.collection(Package.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
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


async def get_packages_by_user_id_and_status(user_id: str, status: PackageStatus) -> List[Package]:
    packages_query = firebase.db.collection(Package.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
        .where(filter=FieldFilter("status", "==", status))

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


async def get_packages_by_user_id(user_id: str) -> List[Package]:
    packages_query = firebase.db.collection(Package.COLLECTION_NAME).where(filter=FieldFilter("user_id", "==", user_id))
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
