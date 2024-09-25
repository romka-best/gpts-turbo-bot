from bot.database.models.subscription import SubscriptionLimit


def get_user_discount(user_discount: int, user_subscription_type) -> int:
    if user_discount > SubscriptionLimit.DISCOUNT[user_subscription_type]:
        return user_discount
    return SubscriptionLimit.DISCOUNT[user_subscription_type]
