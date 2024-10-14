from bot.database.models.common import Quota
from bot.database.models.user import User
from bot.database.operations.user.updaters import update_user, update_user_in_transaction

TEXT_SIMPLE_QUOTA = [Quota.CHAT_GPT4_OMNI_MINI, Quota.CLAUDE_3_HAIKU, Quota.GEMINI_1_FLASH]
TEXT_ADVANCED_QUOTA = [Quota.CHAT_GPT4_OMNI, Quota.CHAT_GPT_O_1_MINI, Quota.CLAUDE_3_SONNET, Quota.GEMINI_1_PRO]
TEXT_SUPER_ADVANCED_QUOTA = [Quota.CHAT_GPT_O_1_PREVIEW, Quota.CLAUDE_3_OPUS, Quota.GEMINI_1_ULTRA]
IMAGE_QUOTA = [Quota.DALL_E, Quota.MIDJOURNEY, Quota.STABLE_DIFFUSION, Quota.FLUX, Quota.FACE_SWAP, Quota.PHOTOSHOP_AI]
MUSIC_QUOTA = [Quota.MUSIC_GEN, Quota.SUNO]


def get_user_with_updated_quota(user: User, user_quota: Quota, quantity_to_delete: int) -> User:
    quantity_deleted = 0
    while quantity_deleted != quantity_to_delete:
        if user.daily_limits[user_quota] != 0:
            chosen_quota = [user_quota]
            if user_quota in TEXT_SIMPLE_QUOTA:
                chosen_quota = TEXT_SIMPLE_QUOTA
            elif user_quota in TEXT_ADVANCED_QUOTA:
                chosen_quota = TEXT_ADVANCED_QUOTA
            elif user_quota in TEXT_SUPER_ADVANCED_QUOTA:
                chosen_quota = TEXT_SUPER_ADVANCED_QUOTA
            elif user_quota in IMAGE_QUOTA:
                chosen_quota = IMAGE_QUOTA
            elif user_quota in MUSIC_QUOTA:
                chosen_quota = MUSIC_QUOTA

            for quota in chosen_quota:
                user.daily_limits[quota] -= 1

            quantity_deleted += 1
        elif user.additional_usage_quota[user_quota] != 0:
            user.additional_usage_quota[user_quota] -= 1
            quantity_deleted += 1
        else:
            break

    return user


async def update_user_usage_quota(user: User, user_quota: Quota, quantity_to_delete: int):
    if quantity_to_delete < 0:
        return

    user = get_user_with_updated_quota(user, user_quota, quantity_to_delete)

    await update_user(user.id, {
        'daily_limits': user.daily_limits,
        'additional_usage_quota': user.additional_usage_quota,
    })


async def update_user_usage_quota_in_transaction(transaction, user: User, user_quota: Quota, quantity_to_delete: int):
    if quantity_to_delete < 0:
        return

    user = get_user_with_updated_quota(user, user_quota, quantity_to_delete)

    await update_user_in_transaction(transaction, user.id, {
        'daily_limits': user.daily_limits,
        'additional_usage_quota': user.additional_usage_quota,
    })
