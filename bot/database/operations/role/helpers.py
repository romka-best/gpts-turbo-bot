from bot.database.main import firebase
from bot.database.models.role import Role
from bot.locales.types import LanguageCode


async def create_role_object(
    translated_names: dict[LanguageCode, str],
    translated_descriptions: dict[LanguageCode, str],
    translated_instructions: dict[LanguageCode, str],
    photo: str,
) -> Role:
    role_ref = firebase.db.collection(Role.COLLECTION_NAME).document()

    return Role(
        id=role_ref.id,
        translated_names=translated_names,
        translated_descriptions=translated_descriptions,
        translated_instructions=translated_instructions,
        photo=photo,
    )
