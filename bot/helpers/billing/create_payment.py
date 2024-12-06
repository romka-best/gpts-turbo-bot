import json
import logging
import uuid
from typing import Optional

import aiohttp
import stripe
from aiohttp import BasicAuth
from pydantic import BaseModel
from yookassa import Configuration

from bot.config import config
from bot.database.models.common import Currency, PaymentMethod
from bot.database.models.product import Product
from bot.database.models.user import User
from bot.helpers.billing.generate_signature import generate_signature
from bot.locales.main import get_localization
from bot.locales.types import LanguageCode

Configuration.account_id = config.YOOKASSA_ACCOUNT_ID.get_secret_value()
Configuration.secret_key = config.YOOKASSA_SECRET_KEY.get_secret_value()
stripe.api_key = config.STRIPE_SECRET_KEY.get_secret_value()

YOOKASSA_URL = 'https://api.yookassa.ru/v3'
PAY_SELECTION_URL = 'https://webform.payselection.com'


class OrderItem(BaseModel):
    product: Product
    price: float
    quantity: Optional[int] = 1


async def create_payment(
    payment_method: PaymentMethod,
    user: User,
    description: str,
    amount: float,
    language_code: LanguageCode,
    is_recurring: bool,
    order_items: list[OrderItem],
    order_id=None,
    order_interval=None,
) -> dict:
    if payment_method == PaymentMethod.YOOKASSA:
        url = f'{YOOKASSA_URL}/payments'
        headers = {
            'Content-Type': 'application/json',
            'Idempotence-Key': str(uuid.uuid4()),
        }
        items = []
        for order_item in order_items:
            product, price, quantity = order_item.product, order_item.price, order_item.quantity
            items.append({
                'amount': {
                    'value': price,
                    'currency': Currency.RUB,
                },
                'description': product.names.get(language_code),
                'vat_code': 1,
                'quantity': quantity,
            })
        payload = {
            'amount': {
                'value': amount,
                'currency': Currency.RUB,
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': config.BOT_URL,
                'locale': 'ru_RU' if language_code == LanguageCode.RU else 'en_US',
            },
            'capture': True,
            'save_payment_method': is_recurring,
            'description': description,
            'merchant_customer_id': user.id,
            'receipt': {
                'customer': {
                    'full_name': user.id,
                    'email': 'me@romandanilov.com',
                },
                'items': items,
            },
        }

        async with aiohttp.ClientSession(
            auth=BasicAuth(Configuration.account_id, Configuration.secret_key)
        ) as session:
            async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
                body = await response.json()
                logging.info(body)
                if response.ok:
                    return body
    elif payment_method == PaymentMethod.PAY_SELECTION:
        url = f'{PAY_SELECTION_URL}/webpayments/paylink_create'
        request_id = str(uuid.uuid4())
        request_body = {
            'MetaData': {
                'PreviewForm': True,
                'OfferUrl': get_localization(language_code).TERMS_LINK,
            },
            'PaymentRequest': {
                'OrderId': order_id,
                'Amount': f'{amount:.2f}',
                'Currency': Currency.USD,
                'Description': description,
                'RebillFlag': is_recurring,
                'ExtraData': {
                    'ReturnUrl': config.BOT_URL,
                    'WebhookUrl': f'{config.WEBHOOK_URL}/payment/pay-selection'
                }
            },
            'CustomerInfo': {
                'Language': language_code,
            },
        }

        request_signature = generate_signature('POST', request_body, request_id)
        request_headers = {
            'X-SITE-ID': config.PAY_SELECTION_SITE_ID.get_secret_value(),
            'X-REQUEST-ID': request_id,
            'X-REQUEST-SIGNATURE': request_signature,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=request_headers, data=json.dumps(request_body)) as response:
                body = await response.json()
                logging.info(body)
                if response.ok:
                    return body
    elif payment_method == PaymentMethod.STRIPE:
        items = []
        for order_item in order_items:
            product, price, quantity = order_item.product, order_item.price, order_item.quantity

            stripe_prices = await stripe.Price.list_async(product=product.stripe_id)
            stripe_price_id = None
            for stripe_price in stripe_prices:
                if stripe_price.currency == Currency.USD.lower() and stripe_price.unit_amount == int(price * 100):
                    stripe_price_id = stripe_price.id
                    break
            if stripe_price_id is None:
                created_stripe_price = await stripe.Price.create_async(
                    product=product.stripe_id,
                    currency=Currency.USD.lower(),
                    unit_amount=int(price * 100),
                    recurring={'interval': order_interval} if is_recurring else None,
                )
                stripe_price_id = created_stripe_price.id

            items.append({
                'price': stripe_price_id,
                'quantity': quantity,
            })
        payment_session = await stripe.checkout.Session.create_async(
            customer=user.stripe_id,
            customer_update={
                'address': 'auto',
                'name': 'auto',
            },
            line_items=items,
            mode='subscription' if is_recurring else 'payment',
            payment_intent_data={
                'metadata': {
                    'order_id': order_id,
                },
            } if not is_recurring else None,
            subscription_data={
                'metadata': {
                    'order_id': order_id,
                },
            } if is_recurring else None,
            automatic_tax={
                'enabled': True,
            },
            adaptive_pricing={
                'enabled': True,
            },
            success_url=config.BOT_URL,
        )
        return payment_session
    else:
        raise NotImplementedError(f'Payment method is not implemented: {payment_method}')
