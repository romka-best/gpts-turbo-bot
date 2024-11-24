from bot.database.main import firebase
from bot.database.models.role import Role
from bot.database.operations.role.helpers import create_role_object


async def write_role(
    name: str,
    translated_names: dict,
    translated_descriptions: dict,
    translated_instructions: dict,
) -> Role:
    role = await create_role_object(name, translated_names, translated_descriptions, translated_instructions)
    await firebase.db.collection(Role.COLLECTION_NAME).document(role.id).set(role.to_dict())

    return role
