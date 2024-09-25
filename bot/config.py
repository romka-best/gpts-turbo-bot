import os
from pathlib import Path
from typing import ClassVar, List, Dict

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class MessageEffect:
    FIRE = 'FIRE'
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'
    HEART = 'HEART'
    CONGRATS = 'CONGRATS'
    POOP = 'POOP'


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

    SUPER_ADMIN_ID: str = '354543567'
    ADMIN_IDS: List[str] = ['354543567', '6078317830']
    DEVELOPER_IDS: List[str] = ['763258583', '5456216473', '789575146']

    CERTIFICATE_NAME: SecretStr
    STORAGE_NAME: SecretStr
    BILLING_TABLE: SecretStr

    BOT_URL: str
    BOT_TOKEN: SecretStr

    MESSAGE_EFFECTS: Dict = {
        MessageEffect.FIRE: '5104841245755180586',  # 🔥
        MessageEffect.LIKE: '5107584321108051014',  # 👍
        MessageEffect.DISLIKE: '5104858069142078462',  # 👎
        MessageEffect.HEART: '5159385139981059251',  # ❤️
        MessageEffect.CONGRATS: '5046509860389126442',  # 🎉
        MessageEffect.POOP: '5046589136895476101',  # 💩
    }
    MESSAGE_STICKERS: Dict = {}

    YOOKASSA_ACCOUNT_ID: SecretStr
    YOOKASSA_SECRET_KEY: SecretStr

    PAY_SELECTION_SITE_ID: SecretStr
    PAY_SELECTION_SECRET_KEY: SecretStr
    PAY_SELECTION_PUBLIC_KEY: SecretStr

    OAUTH_YANDEX_TOKEN: SecretStr
    OPENAI_API_KEY: SecretStr
    ANTHROPIC_API_KEY: SecretStr
    GEMINI_API_KEY: SecretStr
    REPLICATE_API_TOKEN: SecretStr
    MIDJOURNEY_API_TOKEN: SecretStr
    SUNO_TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file=str(BASE_DIR / f'.env.{os.getenv("ENVIRONMENT", "testing")}'),
                                      env_file_encoding='utf-8')


config = Settings()
