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
    DALL_E = 'dall-e'
    MIDJOURNEY = 'midjourney'
    FACE_SWAP = 'face-swap'
    GFPGAN = 'gfpgan'
    MUSIC_GEN = 'music-gen'
    SUNO = 'suno'


class Quota:
    CHAT_GPT3_TURBO = "gpt3"
    CHAT_GPT4_TURBO = "gpt4"
    CHAT_GPT4_OMNI = "gpt4_omni"
    CLAUDE_3_SONNET = "claude_3_sonnet"
    CLAUDE_3_OPUS = "claude_3_opus"
    DALL_E = "dall_e"
    MIDJOURNEY = "midjourney"
    FACE_SWAP = "face_swap"
    GFPGAN = "gfpgan"
    MUSIC_GEN = "music_gen"
    SUNO = "suno"
    ADDITIONAL_CHATS = "additional_chats"
    FAST_MESSAGES = "fast_messages"
    VOICE_MESSAGES = "voice_messages"
    ACCESS_TO_CATALOG = "access_to_catalog"


class ChatGPTVersion:
    V3_Turbo = 'gpt-3.5-turbo'
    V4_Turbo = 'gpt-4-turbo'
    V4_Omni = 'gpt-4o'


class ClaudeGPTVersion:
    V3_Sonnet = 'claude-3-5-sonnet-20240620'
    V3_Opus = 'claude-3-opus-20240229'


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
    # UPSCALE_TWO = "upscale_2x"
    # UPSCALE_FOUR = "upscale_4x"
    # UPSCALE_SUBTLE = "upscale_subtle"
    # UPSCALE_CREATIVE = "upscale_creative"
    VARIATION = "variation"
    # VARY_SUBTLE = "vary_subtle"
    # VARY_STRONG = "vary_strong"
    # ZOOM_OUT_ONE_AND_HALF = "zoom_out_1.5x"
    # ZOOM_OUT_TWO = "zoom_out_2x"
    REROLL = "reroll"


class FaceSwapVersion:
    LATEST = 'LATEST'


class GFPGANVersion:
    LATEST = 'LATEST'


class MusicGenVersion:
    LATEST = 'LATEST'


class SunoMode:
    SIMPLE = "SIMPLE"
    CUSTOM = "CUSTOM"


class SunoSendType:
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"


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


DEFAULT_ROLE = "PERSONAL_ASSISTANT"
