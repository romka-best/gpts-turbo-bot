from enum import StrEnum


class Currency:
    RUB = 'RUB'
    USD = 'USD'
    XTR = 'XTR'

    SYMBOLS = {
        RUB: '₽',
        USD: '$',
        XTR: '⭐️',
    }


class Model:
    CHAT_GPT = 'chat-gpt'
    CLAUDE = 'claude'
    GEMINI = 'gemini'
    EIGHTIFY = 'eightify'
    DALL_E = 'dall-e'
    MIDJOURNEY = 'midjourney'
    STABLE_DIFFUSION = 'stable-diffusion'
    FLUX = 'flux'
    FACE_SWAP = 'face-swap'
    PHOTOSHOP_AI = 'photoshop-ai'
    MUSIC_GEN = 'music-gen'
    SUNO = 'suno'


class ModelType(StrEnum):
    TEXT = 'TEXT'
    SUMMARY = 'SUMMARY'
    IMAGE = 'IMAGE'
    MUSIC = 'MUSIC'
    VIDEO = 'VIDEO'


class Quota:
    CHAT_GPT4_OMNI = 'gpt4_omni'
    CHAT_GPT4_OMNI_MINI = 'gpt4_omni_mini'
    CHAT_GPT_O_1_MINI = 'o1-mini'
    CHAT_GPT_O_1_PREVIEW = 'o1-preview'
    CLAUDE_3_HAIKU = 'claude_3_haiku'
    CLAUDE_3_SONNET = 'claude_3_sonnet'
    CLAUDE_3_OPUS = 'claude_3_opus'
    GEMINI_1_FLASH = 'gemini_1_flash'
    GEMINI_1_PRO = 'gemini_1_pro'
    GEMINI_1_ULTRA = 'gemini_1_ultra'
    EIGHTIFY = 'eightify'
    DALL_E = 'dall_e'
    MIDJOURNEY = 'midjourney'
    STABLE_DIFFUSION = 'stable_diffusion'
    FLUX = 'flux'
    FACE_SWAP = 'face_swap'
    PHOTOSHOP_AI = 'photoshop_ai'
    MUSIC_GEN = 'music_gen'
    SUNO = 'suno'
    ADDITIONAL_CHATS = 'additional_chats'
    FAST_MESSAGES = 'fast_messages'
    VOICE_MESSAGES = 'voice_messages'
    ACCESS_TO_CATALOG = 'access_to_catalog'


class ChatGPTVersion:
    V4_Omni = 'gpt-4o'
    V4_Omni_Mini = 'gpt-4o-mini'
    V1_O_Mini = 'o1-mini'
    V1_O_Preview = 'o1-preview'


class ClaudeGPTVersion:
    V3_Haiku = 'claude-3-5-haiku-latest'
    V3_Sonnet = 'claude-3-5-sonnet-latest'
    V3_Opus = 'claude-3-opus-latest'


class GeminiGPTVersion:
    V1_Flash = 'gemini-1.5-flash'
    V1_Pro = 'gemini-1.5-pro'
    V1_Ultra = 'gemini-1.0-ultra'


class EightifyVersion:
    LATEST = 'LATEST'


class EightifyFocus:
    INSIGHTFUL = 'insightful'
    FUNNY = 'funny'
    ACTIONABLE = 'actionable'
    CONTROVERSIAL = 'controversial'


class EightifyFormat:
    LIST = 'list'
    FAQ = 'faq'


class EightifyAmount:
    AUTO = 'auto'
    SHORT = 'short'
    DETAILED = 'detailed'


class DALLEVersion:
    V2 = 'dall-e-2'
    V3 = 'dall-e-3'


class DALLEResolution:
    LOW = '1024x1024'
    MEDIUM = '1024x1792'
    HIGH = '1792x1024'


class DALLEQuality:
    STANDARD = 'standard'
    HD = 'hd'


class MidjourneyVersion:
    V5 = '5.2'
    V6 = '6.1'


class MidjourneyAction:
    PAYMENT = 'payment'
    IMAGINE = 'imagine'
    UPSCALE = 'upscale'
    # UPSCALE_TWO = 'upscale_2x'
    # UPSCALE_FOUR = 'upscale_4x'
    # UPSCALE_SUBTLE = 'upscale_subtle'
    # UPSCALE_CREATIVE = 'upscale_creative'
    VARIATION = 'variation'
    # VARY_SUBTLE = 'vary_subtle'
    # VARY_STRONG = 'vary_strong'
    # ZOOM_OUT_ONE_AND_HALF = 'zoom_out_1.5x'
    # ZOOM_OUT_TWO = 'zoom_out_2x'
    REROLL = 'reroll'


class StableDiffusionVersion:
    LATEST = 'LATEST'


class FluxVersion:
    LATEST = 'LATEST'


class FluxSafetyTolerance:
    STRICT = 1
    MIDDLE = 3
    PERMISSIVE = 5


class FaceSwapVersion:
    LATEST = 'LATEST'


class PhotoshopAIVersion:
    LATEST = 'LATEST'


class PhotoshopAIAction:
    RESTORATION = 'restoration'
    COLORIZATION = 'colorization'
    REMOVAL_BACKGROUND = 'removal_background'


class MusicGenVersion:
    LATEST = 'LATEST'


class SunoVersion:
    V3 = 'chirp-v3-0'
    V3_5 = 'chirp-v3-5'
    V4 = 'chirp-v4'


class SunoMode:
    SIMPLE = 'SIMPLE'
    CUSTOM = 'CUSTOM'


class AspectRatio:
    SQUARE = '1:1'
    LANDSCAPE = '16:9'
    PORTRAIT = '9:16'
    CINEMASCOPE_HORIZONTAL = '21:9'
    CINEMASCOPE_VERTICAL = '9:21'
    STANDARD_HORIZONTAL = '3:2'
    STANDARD_VERTICAL = '2:3'
    BANNER_HORIZONTAL = '5:4'
    BANNER_VERTICAL = '4:5'
    CLASSIC_HORIZONTAL = '4:3'
    CLASSIC_VERTICAL = '3:4'
    CUSTOM = 'CUSTOM'


class SendType:
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    DOCUMENT = 'DOCUMENT'
    AUDIO = 'AUDIO'
    VIDEO = 'VIDEO'


class PaymentType:
    SUBSCRIPTION = 'SUBSCRIPTION'
    PACKAGE = 'PACKAGE'
    CART = 'CART'


class PaymentMethod:
    YOOKASSA = 'YOOKASSA'
    PAY_SELECTION = 'PAY_SELECTION'
    STRIPE = 'STRIPE'
    TELEGRAM_STARS = 'TELEGRAM_STARS'
    CRYPTO = 'CRYPTO'
    GIFT = 'GIFT'

    _CURRENCY_MAP = {
        YOOKASSA: Currency.RUB,
        PAY_SELECTION: Currency.USD,
        STRIPE: Currency.USD,
        TELEGRAM_STARS: Currency.XTR,
        CRYPTO: None,
        GIFT: None,
    }

    @staticmethod
    def get_currency(payment_method: str):
        return PaymentMethod._CURRENCY_MAP.get(payment_method, Currency.USD)


class UTM:
    SOURCE = 'source'
    MEDIUM = 'medium'
    CAMPAIGN = 'campaign'
    TERM = 'term'
    CONTENT = 'content'
