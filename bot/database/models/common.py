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


class Quota:
    GPT3 = "gpt3"
    GPT4 = "gpt4"
    DALLE3 = "dalle3"
    FACE_SWAP = "face_swap"
    ADDITIONAL_CHATS = "additional_chats"
    FAST_MESSAGES = "fast_messages"
    VOICE_MESSAGES = "voice_messages"
    ACCESS_TO_CATALOG = "access_to_catalog"


class RoleName:
    PERSONAL_ASSISTANT = "PERSONAL_ASSISTANT"
    TUTOR = "TUTOR"
    LANGUAGE_TUTOR = "LANGUAGE_TUTOR"
    CREATIVE_WRITER = "CREATIVE_WRITER"
    TECHNICAL_ADVISOR = "TECHNICAL_ADVISOR"
    MARKETER = "MARKETER"
    SMM_SPECIALIST = "SMM_SPECIALIST"
    CONTENT_SPECIALIST = "CONTENT_SPECIALIST"
    DESIGNER = "DESIGNER"
    SOCIAL_MEDIA_PRODUCER = "SOCIAL_MEDIA_PRODUCER"
    LIFE_COACH = "LIFE_COACH"
    ENTREPRENEUR = "ENTREPRENEUR"
