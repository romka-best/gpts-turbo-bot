class Currency:
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'

    SYMBOLS = {
        RUB: '₽',
        USD: '$',
        EUR: '€'
    }


class Model:
    GPT3 = 'gpt-3.5-turbo-0125'
    GPT4 = 'gpt-4-vision-preview'
    DALLE3 = 'dall-e-3'
    FACE_SWAP = 'face-swap'
    MUSIC_GEN = 'music-gen'


class Quota:
    GPT3 = "gpt3"
    GPT4 = "gpt4"
    DALLE3 = "dalle3"
    FACE_SWAP = "face_swap"
    MUSIC_GEN = "music_gen"
    ADDITIONAL_CHATS = "additional_chats"
    FAST_MESSAGES = "fast_messages"
    VOICE_MESSAGES = "voice_messages"
    ACCESS_TO_CATALOG = "access_to_catalog"


class DALLEResolution:
    LOW = '1024x1024'
    MEDIUM = '1024×1792'
    HIGH = '1792×1024'


class DALLEQuality:
    STANDARD = 'standard'
    HD = 'hd'


class PaymentType:
    SUBSCRIPTION = 'SUBSCRIPTION'
    PACKAGE = 'PACKAGE'
    CART = 'CART'


DEFAULT_ROLE = "PERSONAL_ASSISTANT"
