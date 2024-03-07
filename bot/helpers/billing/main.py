import os

from google.cloud import bigquery
from google.oauth2 import service_account

from bot.config import config

credentials = service_account.Credentials.from_service_account_file(
    os.path.join(config.BASE_DIR, config.CERTIFICATE_NAME.get_secret_value())
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id)
