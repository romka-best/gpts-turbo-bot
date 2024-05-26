class Currency:
    RUB = 'RUB'
    USD = 'USD'

    SYMBOLS = {
        RUB: '₽',
        USD: '$',
    }


class Model:
    CHAT_GPT = 'chat-gpt'
    CLAUDE = 'claude'
    DALL_E = 'dall-e'
    MIDJOURNEY = 'midjourney'
    FACE_SWAP = 'face-swap'
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
    V3_Sonnet = 'claude-3-sonnet-20240229'
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
