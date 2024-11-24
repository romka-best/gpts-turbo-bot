import os
from urllib.parse import quote

from firebase_admin import auth, credentials, initialize_app, firestore_async
from gcloud.aio.auth import Token
from google.cloud.firestore_v1 import AsyncClient
from gcloud.aio.storage import Storage, Bucket

from bot.config import config


class Firebase:
    token: Token
    db: AsyncClient
    storage: Storage
    bucket: Bucket
    auth = None

    def __init__(self):
        self.path_to_credentials = os.path.join(config.BASE_DIR, config.CERTIFICATE_NAME.get_secret_value())

    async def init(self):
        cred = credentials.Certificate(self.path_to_credentials)
        initialize_app(cred, {
            'storageBucket': config.STORAGE_NAME.get_secret_value(),
        })

        scopes = ['https://www.googleapis.com/auth/cloud-platform']
        self.token = Token(service_file=self.path_to_credentials, scopes=scopes)

        self.db = firestore_async.client()
        self.storage = Storage(token=self.token)
        self.bucket = self.storage.get_bucket(config.STORAGE_NAME.get_secret_value())
        self.auth = auth

    async def close(self):
        if self.db:
            self.db.close()
        if self.storage:
            await self.storage.close()

    def get_public_url(self, blob_name: str, query_params='alt=media'):
        blob_name = quote(blob_name, safe='')

        public_url = f'https://firebasestorage.googleapis.com/v0/b/{self.bucket.name}/o/{blob_name}'
        if query_params:
            public_url = f'{public_url}?{query_params}'

        return public_url

    async def delete_blob(self, blob_name: str):
        await self.storage.delete(self.bucket.name, blob_name)


firebase = Firebase()
