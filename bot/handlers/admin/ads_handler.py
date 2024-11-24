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
from bot.keyboards.admin.ads import build_ads_keyboard
from bot.locales.main import get_user_language, get_localization
from bot.states.ads import Ads

ads_router = Router()


async def handle_ads(message: Message, user_id: str, state: FSMContext):
    await state.clear()

    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_ads_keyboard(user_language_code)
    await message.edit_text(
        text=get_localization(user_language_code).ADS_INFO,
        reply_markup=reply_markup,
    )

    await state.set_state(Ads.waiting_for_campaign_name)


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


@ads_router.message(Ads.waiting_for_campaign_name, F.text, ~F.text.startswith('/'))
async def ads_campaign_sent(message: Message, state: FSMContext):
    campaign_name = message.text
    product_cache = {}

    for i in range(10):
        users = await get_users(
            utm={
                UTM.CAMPAIGN: campaign_name,
                UTM.CONTENT: str(i + 1),
            },
        )
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

        await message.answer(
            text=f'''
{i + 1}. {len(users)}
# {len(users) - only_text_users - only_image_users - text_and_image_users} - Не писали ничего
# {only_text_users} - Сделали запрос только в текстовой модели
# {only_image_users} - Сделали запрос только в графической модели
# {text_and_image_users} - Сделали запрос в текстовой и графической моделях
# {clients} - Купили что-то
''',
        )

    await state.clear()
