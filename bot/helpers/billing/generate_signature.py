import hashlib
import hmac

from bot.config import config


def generate_signature(request_method: str, request_body: dict, request_id: str):
    signature_string = (f'{request_method}\n'
                        f'{config.BOT_URL}\n'
                        f'{config.PAY_SELECTION_SITE_ID.get_secret_value()}'
                        f'\n{request_id}\n'
                        f'{request_body}')

    signature = hmac.new(
        key=config.PAY_SELECTION_SECRET_KEY.get_secret_value().encode(),
        msg=signature_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    return signature
