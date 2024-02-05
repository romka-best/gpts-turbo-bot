from datetime import datetime, timezone

from google.cloud import firestore

from bot.database.models.common import Quota
from bot.database.models.package import PackageStatus, PackageType
from bot.database.operations.package import get_package, update_package_in_transaction
from bot.database.operations.user import get_user, update_user_in_transaction


@firestore.async_transactional
async def create_package(transaction,
                         package_id: str,
                         user_id: str,
                         provider_payment_charge_id: str):
    user = await get_user(user_id)
    package = await get_package(package_id)

    await update_package_in_transaction(transaction, package_id, {
        "status": PackageStatus.SUCCESS,
        "provider_payment_charge_id": provider_payment_charge_id,
        "edited_at": datetime.now(timezone.utc),
    })

    if package.type == PackageType.GPT3:
        user.additional_usage_quota[Quota.GPT3] += package.quantity
    elif package.type == PackageType.GPT4:
        user.additional_usage_quota[Quota.GPT4] += package.quantity
    elif package.type == PackageType.DALLE3:
        user.additional_usage_quota[Quota.DALLE3] += package.quantity
    elif package.type == PackageType.FACE_SWAP:
        user.additional_usage_quota[Quota.FACE_SWAP] += package.quantity
    elif package.type == PackageType.MUSIC_GEN:
        user.additional_usage_quota[Quota.MUSIC_GEN] += package.quantity
    elif package.type == PackageType.CHAT:
        user.additional_usage_quota[Quota.ADDITIONAL_CHATS] += package.quantity
    elif package.type == PackageType.FAST_MESSAGES:
        user.additional_usage_quota[Quota.FAST_MESSAGES] = True
    elif package.type == PackageType.ACCESS_TO_CATALOG:
        user.additional_usage_quota[Quota.ACCESS_TO_CATALOG] = True
    elif package.type == PackageType.VOICE_MESSAGES:
        user.additional_usage_quota[Quota.VOICE_MESSAGES] = True

    await update_user_in_transaction(transaction, user_id, {
        "additional_usage_quota": user.additional_usage_quota
    })
