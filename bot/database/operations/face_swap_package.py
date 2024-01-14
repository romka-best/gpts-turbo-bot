from datetime import datetime, timezone
from typing import Optional, Dict, List

from google.cloud.firestore import Query

from bot.database.main import firebase
from bot.database.models.face_swap_package import FaceSwapPackage, UsedFaceSwapPackage, FaceSwapPackageStatus, \
    FaceSwapFileData
from bot.database.models.user import UserGender


async def get_face_swap_package(face_swap_package_id: str) -> Optional[FaceSwapPackage]:
    face_swap_package_ref = firebase.db.collection("face_swap_packages").document(str(face_swap_package_id))
    face_swap_package = await face_swap_package_ref.get()

    if face_swap_package.exists:
        return FaceSwapPackage(**face_swap_package.to_dict())


async def get_face_swap_package_by_name_and_gender(
    name: str,
    gender: UserGender,
) -> Optional[FaceSwapPackage]:
    face_swap_package_stream = firebase.db.collection("face_swap_packages") \
        .where("name", "==", name) \
        .where("gender", "==", gender) \
        .limit(1) \
        .stream()

    async for doc in face_swap_package_stream:
        return FaceSwapPackage(**doc.to_dict())


async def get_face_swap_packages(start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None) -> List[FaceSwapPackage]:
    face_swap_packages_query = firebase.db.collection("face_swap_packages")

    if start_date:
        face_swap_packages_query = face_swap_packages_query.where("created_at", ">=", start_date)
    if end_date:
        face_swap_packages_query = face_swap_packages_query.where("created_at", "<=", end_date)

    face_swap_packages = face_swap_packages_query.order_by("created_at", direction=Query.ASCENDING).stream()
    return [
        FaceSwapPackage(**face_swap_package.to_dict()) async for face_swap_package in face_swap_packages
    ]


async def get_face_swap_packages_by_gender(
    gender: UserGender,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    status: Optional[FaceSwapPackageStatus] = None
) -> List[FaceSwapPackage]:
    face_swap_packages_query = firebase.db.collection("face_swap_packages").where("gender", "==", gender)

    if start_date:
        face_swap_packages_query = face_swap_packages_query.where("created_at", ">=", start_date)
    if end_date:
        face_swap_packages_query = face_swap_packages_query.where("created_at", "<=", end_date)
    if status:
        face_swap_packages_query = face_swap_packages_query.where("status", "==", status)

    face_swap_packages = face_swap_packages_query.order_by("created_at", direction=Query.ASCENDING).stream()
    return [
        FaceSwapPackage(**face_swap_package.to_dict()) async for face_swap_package in face_swap_packages
    ]


async def create_face_swap_package_object(name: str,
                                          translated_names: Dict,
                                          gender: UserGender,
                                          files: List[FaceSwapFileData],
                                          status: FaceSwapPackageStatus) -> FaceSwapPackage:
    face_swap_package_ref = firebase.db.collection('face_swap_packages').document()
    return FaceSwapPackage(
        id=face_swap_package_ref.id,
        name=name,
        translated_names=translated_names,
        gender=gender,
        files=files,
        status=status
    )


async def write_face_swap_package(name: str,
                                  translated_names: Dict,
                                  gender: UserGender,
                                  files: List[FaceSwapFileData],
                                  status: FaceSwapPackageStatus) -> FaceSwapPackage:
    face_swap_package = await create_face_swap_package_object(name, translated_names, gender, files, status)
    await firebase.db.collection('face_swap_packages').document(face_swap_package.id).set(
        face_swap_package.to_dict()
    )

    return face_swap_package


async def update_face_swap_package(face_swap_package_id: str, data: Dict):
    face_swap_package_ref = firebase.db.collection('face_swap_packages').document(face_swap_package_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await face_swap_package_ref.update(data)


async def get_used_face_swap_package(used_face_swap_package_id: str) -> Optional[UsedFaceSwapPackage]:
    used_face_swap_package_ref = firebase.db.collection("used_face_swap_packages").document(
        str(used_face_swap_package_id)
    )
    used_face_swap_package = await used_face_swap_package_ref.get()

    if used_face_swap_package.exists:
        return UsedFaceSwapPackage(**used_face_swap_package.to_dict())


async def get_used_face_swap_package_by_user_id_and_package_id(user_id: str,
                                                               package_id: str) -> Optional[UsedFaceSwapPackage]:
    used_face_swap_package_stream = firebase.db.collection("used_face_swap_packages") \
        .where("user_id", "==", user_id) \
        .where("package_id", "==", package_id) \
        .limit(1) \
        .stream()

    async for doc in used_face_swap_package_stream:
        return UsedFaceSwapPackage(**doc.to_dict())


async def get_used_face_swap_packages_by_user_id(user_id: str) -> List[UsedFaceSwapPackage]:
    used_face_swap_packages_stream = firebase.db.collection("used_face_swap_packages") \
        .where("user_id", "==", user_id) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .stream()
    used_face_swap_packages = [
        UsedFaceSwapPackage(**used_face_swap_package.to_dict()) async for used_face_swap_package in
        used_face_swap_packages_stream
    ]

    return used_face_swap_packages


async def get_used_face_swap_packages(start_date: Optional[datetime] = None,
                                      end_date: Optional[datetime] = None) -> List[UsedFaceSwapPackage]:
    used_face_swap_packages_query = firebase.db.collection("used_face_swap_packages")

    if start_date:
        used_face_swap_packages_query = used_face_swap_packages_query.where("created_at", ">=", start_date)
    if end_date:
        used_face_swap_packages_query = used_face_swap_packages_query.where("created_at", "<=", end_date)

    used_face_swap_packages = used_face_swap_packages_query.stream()
    return [
        UsedFaceSwapPackage(**used_face_swap_package.to_dict()) async for used_face_swap_package in
        used_face_swap_packages
    ]


async def create_used_face_swap_package_object(user_id: str,
                                               package_id: str,
                                               used_images: List[str]) -> UsedFaceSwapPackage:
    used_face_swap_package_ref = firebase.db.collection('used_face_swap_packages').document()
    return UsedFaceSwapPackage(
        id=used_face_swap_package_ref.id,
        user_id=user_id,
        package_id=package_id,
        used_images=used_images
    )


async def write_used_face_swap_package(user_id: str,
                                       package_id: str,
                                       used_images: List[str]) -> UsedFaceSwapPackage:
    used_face_swap_package = await create_used_face_swap_package_object(user_id, package_id, used_images)
    await firebase.db.collection('used_face_swap_packages').document(used_face_swap_package.id).set(
        used_face_swap_package.to_dict()
    )

    return used_face_swap_package


async def update_used_face_swap_package(used_face_swap_package_id: str, data: Dict):
    used_face_swap_package_ref = firebase.db.collection('used_face_swap_packages').document(used_face_swap_package_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await used_face_swap_package_ref.update(data)
