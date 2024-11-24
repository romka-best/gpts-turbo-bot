from bot.database.main import firebase
from bot.database.models.product import ProductType, Product, ProductCategory
from bot.database.operations.product.helpers import create_product_object


async def write_product(
    stripe_id: str,
    is_active: bool,
    type: ProductType,
    category: ProductCategory,
    names: dict,
    descriptions: dict,
    prices: dict,
    photos=None,
    order=-1,
    discount=0,
    details=None,
) -> Product:
    product = await create_product_object(
        stripe_id,
        is_active,
        type,
        category,
        names,
        descriptions,
        prices,
        photos,
        order,
        discount,
        details,
    )
    await firebase.db.collection(Product.COLLECTION_NAME).document(product.id).set(product.to_dict())

    return product
