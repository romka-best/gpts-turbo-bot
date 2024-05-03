class Currency:
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'

    SYMBOLS = {
        RUB: '₽',
        USD: '$',
        EUR: '€',
    }


class Model:
    CHAT_GPT = 'chat-gpt'
    DALL_E = 'dall-e'
    MIDJOURNEY = 'midjourney'
    FACE_SWAP = 'face-swap'
    MUSIC_GEN = 'music-gen'
    SUNO = 'suno'


class Quota:
    CHAT_GPT3 = "gpt3"
    CHAT_GPT4 = "gpt4"
    DALL_E = "dall_e"
    MIDJOURNEY = "midjourney"
    FACE_SWAP = "face_swap"
    MUSIC_GEN = "music_gen"
    SUNO = "suno"
    ADDITIONAL_CHATS = "additional_chats"
    FAST_MESSAGES = "fast_messages"
    VOICE_MESSAGES = "voice_messages"
    ACCESS_TO_CATALOG = "access_to_catalog"


class GPTVersion:
    V3 = 'gpt-3.5-turbo'
    V4 = 'gpt-4-turbo'


class DALLEResolution:
    LOW = '1024x1024'
    MEDIUM = '1024×1792'
    HIGH = '1792×1024'


class DALLEQuality:
    STANDARD = 'standard'
    HD = 'hd'


class DALLEVersion:
    V2 = 'dall-e-2'
    V3 = 'dall-e-3'


class MidjourneyVersion:
    V5 = '5.2'
    V6 = '6.0'


class MidjourneyAction:
    PAYMENT = "payment"
    IMAGINE = "imagine"
    UPSCALE = "upscale"
    VARIATION = "variation"
    REROLL = "reroll"


class SunoMode:
    SIMPLE = "SIMPLE"
    CUSTOM = "CUSTOM"


class SunoSendType:
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"


class PaymentType:
    SUBSCRIPTION = 'SUBSCRIPTION'
    PACKAGE = 'PACKAGE'
    CART = 'CART'


DEFAULT_ROLE = "PERSONAL_ASSISTANT"
