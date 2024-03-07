from datetime import datetime, timezone
from typing import Dict

from bot.database.main import firebase
from bot.database.models.face_swap_package import FaceSwapPackage, UsedFaceSwapPackage


async def update_face_swap_package(face_swap_package_id: str, data: Dict):
    face_swap_package_ref = firebase.db.collection(FaceSwapPackage.COLLECTION_NAME) \
        .document(face_swap_package_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await face_swap_package_ref.update(data)


async def update_used_face_swap_package(used_face_swap_package_id: str, data: Dict):
    used_face_swap_package_ref = firebase.db.collection(UsedFaceSwapPackage.COLLECTION_NAME) \
        .document(used_face_swap_package_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await used_face_swap_package_ref.update(data)
