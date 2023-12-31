import os
import firebase_admin
from firebase_admin import credentials, firestore_async, storage

from bot.config import config

path_to_credentials = os.path.join(config.BASE_DIR, config.CERTIFICATE_NAME.get_secret_value())

cred = credentials.Certificate(path_to_credentials)

default_app = firebase_admin.initialize_app(cred, {
    'storageBucket': config.STORAGE_NAME.get_secret_value(),
})

db = firestore_async.client()
bucket = storage.bucket()
