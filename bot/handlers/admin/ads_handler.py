import re
from urllib.parse import urlparse, parse_qs

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import UTM
from bot.database.models.product import ProductCategory
from bot.database.models.transaction import Transaction, TransactionType
from bot.database.operations.product.getters import get_product
from bot.database.operations.user.getters import get_users
from bot.keyboards.admin.admin import build_admin_keyboard
from bot.keyboards.admin.ads import (
    build_ads_keyboard,
    build_ads_get_keyboard,
    build_ads_create_keyboard,
    build_ads_create_choose_source_keyboard,
    build_ads_create_choose_medium_keyboard,
)
from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_user_language, get_localization
from bot.states.admin.ads import Ads

ads_router = Router()


async def handle_ads(message: Message, user_id: str, state: FSMContext):
    await state.clear()

    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_ads_keyboard(user_language_code)
    await message.edit_text(
        text=get_localization(user_language_code).ADMIN_ADS_INFO,
        reply_markup=reply_markup,
    )


@ads_router.callback_query(lambda c: c.data.startswith('ads:'))
async def handle_ads_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'back':
        reply_markup = build_admin_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_INFO,
            reply_markup=reply_markup,
        )

        await state.clear()
        return
    elif action == 'create':
        reply_markup = build_ads_create_choose_source_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_ADS_CHOOSE_SOURCE,
            reply_markup=reply_markup,
        )
    elif action == 'get':
        reply_markup = build_ads_get_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_ADS_SEND_LINK,
            reply_markup=reply_markup,
        )

        await state.set_state(Ads.waiting_for_link)


@ads_router.callback_query(lambda c: c.data.startswith('ads_create_choose_source:'))
async def handle_ads_create_choose_source_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'back':
        reply_markup = build_ads_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_ADS_INFO,
            reply_markup=reply_markup,
        )
    else:
        reply_markup = build_ads_create_choose_medium_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_ADS_CHOOSE_MEDIUM,
            reply_markup=reply_markup,
        )

        await state.update_data(source=action)


@ads_router.callback_query(lambda c: c.data.startswith('ads_create_choose_medium:'))
async def handle_ads_create_choose_source_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'back':
        reply_markup = build_ads_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_ADS_INFO,
            reply_markup=reply_markup,
        )
    else:
        reply_markup = build_ads_create_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_ADS_SEND_NAME,
            reply_markup=reply_markup,
        )

        await state.update_data(medium=action)
        await state.set_state(Ads.waiting_for_campaign_name)


@ads_router.message(Ads.waiting_for_campaign_name, F.text, ~F.text.startswith('/'))
async def ads_campaign_name_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    campaign_name = message.text
    if re.match(r'^[a-zA-Z]+$', campaign_name):
        reply_markup = build_ads_create_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).ADMIN_ADS_SEND_QUANTITY,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )
        await state.update_data(name=campaign_name)
        await state.set_state(Ads.waiting_for_quantity)
    else:
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).ADMIN_ADS_VALUE_ERROR,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )


@ads_router.message(Ads.waiting_for_quantity, F.text, ~F.text.startswith('/'))
async def ads_quantity_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)
    user_data = await state.get_data()

    try:
        quantity = int(message.text)
        source, medium, name = user_data.get('source'), user_data.get('medium'), user_data.get('name')
        urls = []
        for i in range(quantity):
            utm = {
                UTM.SOURCE: source,
                UTM.MEDIUM: medium,
                UTM.CAMPAIGN: name,
                UTM.CONTENT: i + 1,
            }
            start_value = '_'.join(f'{key}-{value}' for key, value in utm.items())
            final_url = f'{config.BOT_URL}?start={start_value}'
            urls.append(final_url)
        await message.answer(
            text='\n'.join(urls),
        )
        await state.clear()
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).ERROR_IS_NOT_NUMBER,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )


@ads_router.callback_query(lambda c: c.data.startswith('ads_create:'))
async def handle_ads_create_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'back':
        reply_markup = build_ads_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_ADS_INFO,
            reply_markup=reply_markup,
        )

        await state.clear()


@ads_router.message(Ads.waiting_for_link, F.text, ~F.text.startswith('/'))
async def ads_link_sent(message: Message, state: FSMContext):
    parsed_url = urlparse(message.text)
    params = parse_qs(parsed_url.query)
    start_param = params.get('start', [''])[0]
    utm_parts = dict(item.split('-', 1) for item in start_param.split('_') if '-' in item)

    users = await get_users(
        utm=utm_parts,
    )

    product_cache = {}

    only_text_users = 0
    only_image_users = 0
    text_and_image_users = 0
    clients = 0
    for user in users:
        has_text_requests = False
        has_image_requests = False
        has_purchases = False

        transactions_query = (
            firebase.db.collection(Transaction.COLLECTION_NAME)
            .where('user_id', '==', user.id)
            .order_by('created_at')
            .limit(config.BATCH_SIZE)
        )

        is_running = True
        last_doc = None

        while is_running:
            if last_doc:
                transactions_query = transactions_query.start_after(last_doc)

            docs = transactions_query.stream()

            count = 0
            async for doc in docs:
                count += 1

                transaction = Transaction(**doc.to_dict())

                if transaction.type == TransactionType.INCOME:
                    has_purchases = True
                elif transaction.type == TransactionType.EXPENSE:
                    if transaction.product_id not in product_cache:
                        transaction_product = await get_product(transaction.product_id)
                        product_cache[transaction.product_id] = transaction_product
                    else:
                        transaction_product = product_cache[transaction.product_id]
                    if transaction_product.category == ProductCategory.TEXT:
                        has_text_requests = True
                    elif transaction_product.category == ProductCategory.IMAGE:
                        has_image_requests = True

            if count < config.BATCH_SIZE:
                is_running = False
                break

            last_doc = doc

        if has_purchases:
            clients += 1

        if has_text_requests and has_image_requests:
            text_and_image_users += 1
        elif has_text_requests:
            only_text_users += 1
        elif has_image_requests:
            only_image_users += 1

    await message.answer(text=f'''
📯 <i>{utm_parts[UTM.CAMPAIGN]}</i>. <b>{len(users)}</b>
┣ <b>{len(users) - only_text_users - only_image_users - text_and_image_users}</b> - Не писали ничего
┣ <b>{only_text_users}</b> - Сделали запрос только в текстовой модели
┣ <b>{only_image_users}</b> - Сделали запрос только в графической модели
┣ <b>{text_and_image_users}</b> - Сделали запрос в текстовой и графической моделях
┗ <b>{clients}</b> - Купили что-то
''')

    await state.clear()
