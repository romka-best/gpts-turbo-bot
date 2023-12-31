from datetime import datetime, timezone
from typing import Dict

from bot.database.models.user import UserGender


class FaceSwapPackageName:
    CELEBRITIES = {
        "name": "CELEBRITIES",
        f"{UserGender.MALE}_files": [
            '1_ElonMusk.jpeg',
            '2_LeonardoDiCaprio.jpg',
            '3_ArnoldSchwarzenegger.jpeg',
            '4_JimKerry.jpg',
            '5_RobertDauniJr.jpg',
            '6_DanielRadcliffe.jpeg',
            '7_JohnyDepp.jpg',
            '8_ChrisEvans.jpeg',
            '9_TomCruise.jpeg',
            '10_BradPitt.jpg',
        ],
        f"{UserGender.FEMALE}_files": [
            '1_Beyonce.jpeg',
            '2_EmmaWatson.jpeg',
            '3_CameronDiaz.jpeg',
            '4_KateWinslet.jpeg',
            '5_NataliePortman.jpeg',
            '6_AngelinaJolie.jpeg',
            '7_ScarlettJohansson.jpeg',
            '8_AnneHathaway.jpeg',
            '9_JessicaAlba.jpeg',
            '10_KeiraKnightley.jpeg',
        ]
    }
    MOVIE_CHARACTERS = {
        "name": "MOVIE_CHARACTERS",
        f"{UserGender.MALE}_files": [
            '1_IndianaJones.jpeg',
            '2_JamesBond.jpeg',
            '3_HanSolo.jpeg',
            '4_Joker.jpeg',
            '5_Batman.jpeg',
        ],
        f"{UserGender.FEMALE}_files": [
            '1_Bride.jpeg',
            '2_AmyDunne.png',
            '3_AmeliePoulain.jpeg',
            '4_KatnissEverdeen.jpeg',
            '5_Wednesday.jpeg',
        ]
    }
    PROFESSIONS = {
        "name": "PROFESSIONS",
        f"{UserGender.MALE}_files": [
            '1_Driver.jpeg',
            '2_Accountant.jpeg',
            '3_Programmer.jpeg',
            '4_Doctor.jpeg',
            '5_Cook.jpeg',
        ],
        f"{UserGender.FEMALE}_files": [
            '1_Driver.jpeg',
            '2_Accountant.jpeg',
            '3_Programmer.png',
            '4_Doctor.jpeg',
            '5_Cook.jpeg',
        ]
    }
    SEVEN_WONDERS_OF_THE_ANCIENT_WORLD = {
        "name": "SEVEN_WONDERS_OF_THE_ANCIENT_WORLD",
        f"{UserGender.MALE}_files": [
            '1_GreatPyramidOfGiza.png',
            '2_ColossusOfRhodes.png',
            '3_HangingGardensOfBabylon.png',
            '4_LighthouseOfAlexandria.png',
            '5_MausoleumAtHalicarnassus.png',
            '6_StatueOfZeusAtOlympia.png',
            '7_TempleOfArtemisAtEphesus.png',
        ],
        f"{UserGender.FEMALE}_files": [
            '1_GreatPyramidOfGiza.png',
            '2_ColossusOfRhodes.png',
            '3_HangingGardensOfBabylon.png',
            '4_LighthouseOfAlexandria.png',
            '5_MausoleumAtHalicarnassus.png',
            '6_StatueOfZeusAtOlympia.png',
            '7_TempleOfArtemisAtEphesus.png',
        ]
    }


class FaceSwapPackage:
    id: str
    user_id: str
    name: str
    used_images: Dict
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 user_id: str,
                 name: str,
                 used_images: Dict,
                 created_at=None,
                 edited_at=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.used_images = used_images

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'used_images': self.used_images,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }
