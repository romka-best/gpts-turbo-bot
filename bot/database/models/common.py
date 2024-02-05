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
    GPT3 = 'gpt-3.5-turbo-1106'
    GPT4 = 'gpt-4-1106-preview'
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


DEFAULT_ROLE = "PERSONAL_ASSISTANT"
