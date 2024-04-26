from datetime import datetime
from typing import Optional, List

from google.cloud.firestore_v1 import FieldFilter

from bot.database.main import firebase
from bot.database.models.transaction import Transaction, ServiceType


async def get_transaction(transaction_id: str) -> Optional[Transaction]:
    transaction_ref = firebase.db.collection(Transaction.COLLECTION_NAME).document(str(transaction_id))
    transaction = await transaction_ref.get()

    if transaction.exists:
        transaction_dict = transaction.to_dict()
        return Transaction(
            id=transaction_dict.get('id'),
            user_id=transaction_dict.get('user_id'),
            type=transaction_dict.get('type'),
            service=transaction_dict.get('service'),
            amount=transaction_dict.get('amount'),
            currency=transaction_dict.get('currency'),
            quantity=transaction_dict.get('quantity'),
            details=transaction_dict.get('details'),
            created_at=transaction_dict.get('created_at'),
            edited_at=transaction_dict.get('edited_at'),
        )


async def get_transactions_by_service_and_created_time(
    service: ServiceType,
    created_time: datetime,
) -> List[Transaction]:
    start_date = created_time.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end_date = created_time.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999,
    )

    transaction_stream = firebase.db.collection(Transaction.COLLECTION_NAME) \
        .where(filter=FieldFilter("service", "==", service)) \
        .where(filter=FieldFilter("created_at", ">=", start_date)) \
        .where(filter=FieldFilter("created_at", "<=", end_date)) \
        .stream()

    transactions = [
        Transaction(
            id=transaction.to_dict().get('id'),
            user_id=transaction.to_dict().get('user_id'),
            type=transaction.to_dict().get('type'),
            service=transaction.to_dict().get('service'),
            amount=transaction.to_dict().get('amount'),
            currency=transaction.to_dict().get('currency'),
            quantity=transaction.to_dict().get('quantity'),
            details=transaction.to_dict().get('details'),
            created_at=transaction.to_dict().get('created_at'),
            edited_at=transaction.to_dict().get('edited_at'),
        ) async for transaction in transaction_stream
    ]

    return transactions


async def get_transactions(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[Transaction]:
    transactions_query = firebase.db.collection(Transaction.COLLECTION_NAME)

    if start_date:
        transactions_query = transactions_query.where(filter=FieldFilter("created_at", ">=", start_date))
    if end_date:
        transactions_query = transactions_query.where(filter=FieldFilter("created_at", "<=", end_date))

    transactions = transactions_query.stream()
    return [
        Transaction(
            id=transaction.to_dict().get('id'),
            user_id=transaction.to_dict().get('user_id'),
            type=transaction.to_dict().get('type'),
            service=transaction.to_dict().get('service'),
            amount=transaction.to_dict().get('amount'),
            currency=transaction.to_dict().get('currency'),
            quantity=transaction.to_dict().get('quantity'),
            details=transaction.to_dict().get('details'),
            created_at=transaction.to_dict().get('created_at'),
            edited_at=transaction.to_dict().get('edited_at'),
        ) async for transaction in transactions
    ]
