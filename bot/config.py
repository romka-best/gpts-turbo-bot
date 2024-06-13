import os
from pathlib import Path
from typing import ClassVar, List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent

    WEBHOOK_URL: str
    WEBHOOK_REPLICATE_PATH: str
    WEBHOOK_MIDJOURNEY_PATH: str
    REDIS_URL: str

    MAX_RETRIES: int = 2
    USER_BATCH_SIZE: int = 500
    LIMIT_BETWEEN_REQUESTS_SECONDS: int = 30
    LIMIT_PROCESSING_SECONDS: int = 60
    MODERATOR_ID: str = "354543567"
    ADMIN_CHAT_IDS: List[str] = ["354543567", "6078317830"]

    CERTIFICATE_NAME: SecretStr
    STORAGE_NAME: SecretStr
    BILLING_TABLE: SecretStr

    BOT_URL: str
    BOT_TOKEN: SecretStr

    YOOKASSA_TOKEN: SecretStr
    YOOKASSA_ACCOUNT_ID: SecretStr
    YOOKASSA_SECRET_KEY: SecretStr

    PAY_SELECTION_SITE_ID: SecretStr
    PAY_SELECTION_SECRET_KEY: SecretStr
    PAY_SELECTION_PUBLIC_KEY: SecretStr

    OAUTH_YANDEX_TOKEN: SecretStr
    OPENAI_API_KEY: SecretStr
    ANTHROPIC_API_KEY: SecretStr
    REPLICATE_API_TOKEN: SecretStr
    MIDJOURNEY_API_TOKEN: SecretStr
    SUNO_TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file=str(BASE_DIR / f'.env.{os.getenv("ENVIRONMENT", "testing")}'),
                                      env_file_encoding='utf-8')


config = Settings()
