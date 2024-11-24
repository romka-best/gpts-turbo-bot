from bot.database.main import firebase
from bot.database.models.common import Currency
from bot.database.models.transaction import Transaction, TransactionType


async def create_transaction_object(
    user_id: str,
    type: TransactionType,
    product_id: str,
    amount: float,
    clear_amount: float,
    currency: Currency,
    quantity=1,
    details=None,
    created_at=None,
) -> Transaction:
    transaction_ref = firebase.db.collection(Transaction.COLLECTION_NAME).document()
    return Transaction(
        id=transaction_ref.id,
        user_id=user_id,
        type=type,
        product_id=product_id,
        amount=amount,
        clear_amount=clear_amount,
        currency=currency,
        quantity=quantity,
        details=details,
        created_at=created_at,
    )
