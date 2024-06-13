from google.cloud import firestore

from bot.database.models.package import Package, PackageStatus
from bot.database.operations.package.getters import get_package
from bot.database.operations.package.updaters import update_package_in_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user_in_transaction


@firestore.async_transactional
async def create_package(
    transaction,
    package_id: str,
    user_id: str,
    income_amount: float,
    provider_payment_charge_id: str,
):
    user = await get_user(user_id)
    package = await get_package(package_id)

    await update_package_in_transaction(
        transaction,
        package_id,
        {
            "status": PackageStatus.SUCCESS,
            "income_amount": income_amount,
            "provider_payment_charge_id": provider_payment_charge_id,
        },
    )

    _, user.additional_usage_quota = Package.get_service_type_and_update_quota(
        package.type,
        user.additional_usage_quota,
        package.quantity,
    )

    await update_user_in_transaction(transaction, user_id, {
        "additional_usage_quota": user.additional_usage_quota
    })
