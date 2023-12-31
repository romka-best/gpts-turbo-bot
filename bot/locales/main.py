from typing import Dict, Type

from . import en, ru
from .texts import Texts

localization_classes: Dict[str, Type[Texts]] = {
    'en': en.English,
    'ru': ru.Russian
}


def get_localization(language_code: str) -> Texts:
    localization_class = localization_classes.get(language_code, en.English)
    return localization_class()
