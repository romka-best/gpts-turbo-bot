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
    DALL_E = 'dall-e'
    MIDJOURNEY = 'midjourney'
    STABLE_DIFFUSION = 'stable-diffusion'
    FLUX = 'flux'
    FACE_SWAP = 'face-swap'
    PHOTOSHOP_AI = 'photoshop-ai'
    MUSIC_GEN = 'music-gen'
    SUNO = 'suno'


class ModelType:
    TEXT = 'TEXT'
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
    V3_Haiku = 'claude-3-haiku-20240307'
    V3_Sonnet = 'claude-3-5-sonnet-20240620'
    V3_Opus = 'claude-3-opus-20240229'


class GeminiGPTVersion:
    V1_Flash = 'gemini-1.5-flash'
    V1_Pro = 'gemini-1.5-pro'
    V1_Ultra = 'gemini-1.0-ultra'


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


class SunoMode:
    SIMPLE = 'SIMPLE'
    CUSTOM = 'CUSTOM'


class SunoSendType:
    VIDEO = 'VIDEO'
    AUDIO = 'AUDIO'


class SunoVersion:
    V3 = 'chirp-v3-0'
    V3_5 = 'chirp-v3-5'


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


DEFAULT_ROLE = 'PERSONAL_ASSISTANT'
