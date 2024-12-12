from datetime import timedelta, datetime, timezone

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile, User as TelegramUser

from bot.database.main import firebase
from bot.database.models.common import Model, Currency
from bot.database.models.subscription import SubscriptionStatus, SUBSCRIPTION_FREE_LIMITS
from bot.database.models.user import UserGender, UserSettings
from bot.database.operations.product.getters import get_product
from bot.database.operations.subscription.getters import get_subscription
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.ai.face_swap_handler import handle_face_swap
from bot.handlers.payment.bonus_handler import handle_bonus
from bot.handlers.payment.payment_handler import (
    handle_subscribe,
    handle_package,
    handle_cancel_subscription,
    handle_renew_subscription,
)
from bot.handlers.settings.settings_handler import handle_settings
from bot.keyboards.common.common import build_cancel_keyboard
from bot.keyboards.common.profile import (
    build_profile_keyboard,
    build_profile_quota_keyboard,
    build_profile_gender_keyboard,
)
from bot.locales.main import get_localization, get_user_language
from bot.states.profile import Profile

profile_router = Router()


@profile_router.message(Command('profile'))
async def profile(message: Message, state: FSMContext):
    await state.clear()

    await handle_profile(message, state, message.from_user, False)


async def handle_profile(message: Message, state: FSMContext, telegram_user: TelegramUser, is_edit=False):
    user = await get_user(str(telegram_user.id))
    user_language_code = await get_user_language(str(telegram_user.id), state.storage)

    if (
        user.first_name != telegram_user.first_name or
        user.last_name != telegram_user.last_name or
        user.username != telegram_user.username or
        user.is_premium != telegram_user.is_premium or
        user.language_code != telegram_user.language_code
    ):
        await update_user(user.id, {
            'first_name': telegram_user.first_name,
            'last_name': telegram_user.last_name or '',
            'username': telegram_user.username,
            'is_premium': telegram_user.is_premium or False,
            'language_code': telegram_user.language_code,
        })

    subscription = await get_subscription(user.subscription_id)
    if subscription:
        product_subscription = await get_product(subscription.product_id)
        subscription_name = product_subscription.names.get(user_language_code)
    else:
        subscription_name = '🆓'
    renewal_date = (user.last_subscription_limit_update + timedelta(days=30))

    text = get_localization(user_language_code).profile(
        subscription_name,
        subscription.status if subscription else SubscriptionStatus.ACTIVE,
        user.gender,
        user.current_model,
        user.settings[user.current_model][UserSettings.VERSION],
        user.currency,
        renewal_date.strftime('%d.%m.%Y'),
    )

    blobs = await firebase.bucket.list_blobs(prefix=f'users/avatars/{user.id}.')
    photo_path = blobs[-1]
    try:
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        reply_markup = build_profile_keyboard(
            user_language_code,
            True,
            user.gender != UserGender.UNSPECIFIED,
            subscription.status == SubscriptionStatus.ACTIVE if subscription else False,
            subscription.status == SubscriptionStatus.CANCELED if subscription else False,
        )
        if is_edit:
            await message.edit_caption(
                caption=text,
                reply_markup=reply_markup,
            )
        else:
            await message.answer_photo(
                photo=URLInputFile(photo_link, filename=photo_path, timeout=300),
                caption=text,
                reply_markup=reply_markup,
            )
    except aiohttp.ClientResponseError:
        reply_markup = build_profile_keyboard(
            user_language_code,
            False,
            user.gender != UserGender.UNSPECIFIED,
            subscription.status == SubscriptionStatus.ACTIVE if subscription else False,
            subscription.status == SubscriptionStatus.CANCELED if subscription else False,
        )
        if is_edit:
            await message.edit_text(
                text=text,
                reply_markup=reply_markup,
            )
        else:
            await message.answer(
                text=text,
                reply_markup=reply_markup,
            )


@profile_router.callback_query(lambda c: c.data.startswith('profile:'))
async def handle_profile_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]

    if action == 'open_settings':
        await handle_settings(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'show_quota':
        user = await get_user(user_id)

        current_date = datetime.now(timezone.utc)
        update_date = datetime(
            current_date.year,
            current_date.month,
            current_date.day,
            tzinfo=timezone.utc
        ) + timedelta(days=1, hours=6)
        time_left = update_date - current_date
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes = remainder // 60

        user_subscription = await get_subscription(user.subscription_id)
        if user_subscription:
            product_subscription = await get_product(user_subscription.product_id)
            limits = product_subscription.details.get('limits')
        else:
            limits = SUBSCRIPTION_FREE_LIMITS
        text = get_localization(user_language_code).profile_quota(
            limits,
            user.daily_limits,
            user.additional_usage_quota,
            hours,
            minutes,
        )
        reply_markup = build_profile_quota_keyboard(user_language_code)
        await callback_query.message.reply(
            text=text,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )
    elif action == 'change_photo':
        photo_path = 'users/avatars/example.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        reply_markup = build_cancel_keyboard(user_language_code)
        await callback_query.message.reply_photo(
            photo=URLInputFile(photo_link, filename=photo_path, timeout=300),
            caption=get_localization(user_language_code).SEND_ME_YOUR_PICTURE,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )

        await state.set_state(Profile.waiting_for_photo)
    elif action == 'change_gender':
        reply_markup = build_profile_gender_keyboard(user_language_code)
        await callback_query.message.reply(
            text=get_localization(user_language_code).TELL_ME_YOUR_GENDER,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )
    elif action == 'change_currency':
        user = await get_user(user_id)

        if user.currency == Currency.RUB:
            user.currency = Currency.USD
        elif user.currency == Currency.USD:
            user.currency = Currency.XTR
        else:
            user.currency = Currency.RUB
        await update_user(
            user_id,
            {
                'currency': user.currency,
            }
        )

        await handle_profile(callback_query.message, state, callback_query.from_user, True)
    elif action == 'open_bonus_info':
        await handle_bonus(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'open_buy_subscriptions_info':
        await handle_subscribe(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'open_buy_packages_info':
        await handle_package(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'cancel_subscription':
        await handle_cancel_subscription(callback_query.message, str(callback_query.from_user.id), state)
    elif action == 'renew_subscription':
        await handle_renew_subscription(callback_query.message, str(callback_query.from_user.id), state)


@profile_router.callback_query(lambda c: c.data.startswith('profile_gender:'))
async def handle_profile_gender_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))
    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    gender = callback_query.data.split(':')[1]

    if user.gender != gender:
        user.gender = gender
        await update_user(user.id, {
            'gender': user.gender,
        })

    text_your_gender = get_localization(user_language_code).YOUR_GENDER
    text_gender_male = get_localization(user_language_code).MALE
    text_gender_female = get_localization(user_language_code).FEMALE
    await callback_query.message.edit_text(
        f'{text_your_gender} {text_gender_male if user.gender == UserGender.MALE else text_gender_female}'
    )

    if user.current_model == Model.FACE_SWAP:
        await handle_face_swap(
            callback_query.bot,
            str(callback_query.message.chat.id),
            state,
            str(callback_query.from_user.id),
        )
