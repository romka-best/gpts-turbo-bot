from typing import Dict

from bot.database.main import firebase
from bot.database.models.role import Role


async def create_role_object(
    name: str,
    translated_names: Dict,
    translated_descriptions: Dict,
    translated_instructions: Dict,
) -> Role:
    role_ref = firebase.db.collection(Role.COLLECTION_NAME).document()

    return Role(
        id=role_ref.id,
        name=name,
        translated_names=translated_names,
        translated_descriptions=translated_descriptions,
        translated_instructions=translated_instructions,
    )
