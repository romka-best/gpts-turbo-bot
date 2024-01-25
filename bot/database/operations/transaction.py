from datetime import datetime, timezone
from typing import Optional, Dict, List

from bot.database.main import firebase
from bot.database.models.common import Currency
from bot.database.models.transaction import Transaction, TransactionType, ServiceType


async def get_transaction(transaction_id: str) -> Optional[Transaction]:
    transaction_ref = firebase.db.collection("transactions").document(str(transaction_id))
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


async def get_transactions(start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Transaction]:
    transactions_query = firebase.db.collection("transactions")

    if start_date:
        transactions_query = transactions_query.where("created_at", ">=", start_date)
    if end_date:
        transactions_query = transactions_query.where("created_at", "<=", end_date)

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


async def create_transaction_object(user_id: str,
                                    type: TransactionType,
                                    service: ServiceType,
                                    amount: float,
                                    currency: Currency,
                                    quantity=1,
                                    details=None,
                                    created_at=None) -> Transaction:
    transaction_ref = firebase.db.collection('transactions').document()
    return Transaction(
        id=transaction_ref.id,
        user_id=user_id,
        type=type,
        service=service,
        amount=amount,
        currency=currency,
        quantity=quantity,
        details=details,
        created_at=created_at,
    )


async def write_transaction(user_id: str,
                            type: TransactionType,
                            service: ServiceType,
                            amount: float,
                            currency: Currency,
                            quantity=1,
                            details=None,
                            created_at=None) -> Transaction:
    transaction = await create_transaction_object(user_id,
                                                  type,
                                                  service,
                                                  amount,
                                                  currency,
                                                  quantity,
                                                  details,
                                                  created_at)
    await firebase.db.collection('transactions').document(transaction.id).set(transaction.to_dict())

    return transaction


async def write_transaction_in_transaction(transaction,
                                           user_id: str,
                                           type: TransactionType,
                                           service: ServiceType,
                                           amount: float,
                                           currency: Currency,
                                           quantity=1,
                                           details=None,
                                           created_at=None) -> Transaction:
    transaction_object = await create_transaction_object(user_id,
                                                         type,
                                                         service,
                                                         amount,
                                                         currency,
                                                         quantity,
                                                         details,
                                                         created_at)
    transaction.set(firebase.db.collection('transactions').document(transaction_object.id),
                    transaction_object.to_dict())

    return transaction_object


async def update_transaction(transaction_id: str, data: Dict):
    transaction_ref = firebase.db.collection('transactions').document(transaction_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await transaction_ref.update(data)
