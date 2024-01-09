from datetime import datetime, timezone
from typing import Optional, Dict, List

from google.cloud.firestore import Query

from bot.database.main import firebase
from bot.database.models.role import Role


async def get_role(role_id: str) -> Optional[Role]:
    role_ref = firebase.db.collection("roles").document(role_id)
    role = await role_ref.get()

    if role.exists:
        return Role(**role.to_dict())


async def get_role_by_name(name: str) -> Optional[Role]:
    role_stream = firebase.db.collection("roles") \
        .where("name", "==", name) \
        .limit(1) \
        .stream()

    async for doc in role_stream:
        return Role(**doc.to_dict())


async def get_roles(start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[Role]:
    roles_query = firebase.db.collection("roles")

    if start_date:
        roles_query = roles_query.where("created_at", ">=", start_date)
    if end_date:
        roles_query = roles_query.where("created_at", "<=", end_date)

    roles = roles_query.order_by("created_at", direction=Query.ASCENDING).stream()
    return [
        Role(**role.to_dict()) async for role in roles
    ]


async def create_role_object(name: str,
                             translated_names: Dict,
                             translated_descriptions: Dict,
                             translated_instructions: Dict) -> Role:
    role_ref = firebase.db.collection('roles').document()

    return Role(
        id=role_ref.id,
        name=name,
        translated_names=translated_names,
        translated_descriptions=translated_descriptions,
        translated_instructions=translated_instructions,
    )


async def write_role(name: str,
                     translated_names: Dict,
                     translated_descriptions: Dict,
                     translated_instructions: Dict) -> Role:
    role = await create_role_object(name, translated_names, translated_descriptions, translated_instructions)
    await firebase.db.collection('roles').document(role.id).set(role.to_dict())

    return role


async def update_role(role_id: str, data: Dict):
    role_ref = firebase.db.collection('roles').document(role_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await role_ref.update(data)
