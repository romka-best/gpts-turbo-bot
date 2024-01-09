from bot.database.models.face_swap_package import FaceSwapPackageStatus
from bot.database.models.user import UserGender
from bot.database.operations.face_swap_package import write_face_swap_package, get_face_swap_package_by_name_and_gender


class FaceSwapPackageInfo:
    CELEBRITIES = {
        "name": "CELEBRITIES",
        "translated_names": {
            "en": 'Celebrities ⭐️',
            "ru": 'Знаменитости ⭐'
        },
        f"{UserGender.MALE}_files": [
            {
                'name': '1_ElonMusk.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '2_LeonardoDiCaprio.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '3_ArnoldSchwarzenegger.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '4_JimKerry.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '5_RobertDauniJr.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '6_DanielRadcliffe.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '7_JohnyDepp.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '8_ChrisEvans.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '9_TomCruise.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '10_BradPitt.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '11_TomHanks.png',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '12_HughJackman.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '13_DenzelWashington.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '14_RyanReynolds.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '15_RyanGosling.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '16_DwayneJohnson.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '17_MorganFreeman.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '18_BenedictCumberbatch.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '19_DanielCraig.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '20_MarkWahlberg.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
        ],
        f"{UserGender.FEMALE}_files": [
            {
                'name': '1_Beyonce.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '2_EmmaWatson.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '3_CameronDiaz.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '4_KateWinslet.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '5_NataliePortman.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '6_AngelinaJolie.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '7_ScarlettJohansson.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '8_AnneHathaway.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '9_JessicaAlba.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '10_KeiraKnightley.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '11_LadyGaga.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '12_TaylorSwift.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '13_Rihanna.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '14_JenniferLawrence.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '15_KimKardashian.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '16_KristenStewart.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '17_JenniferAniston.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '18_SelenaGomez.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '19_NickiMinaj.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '20_KatyPerry.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
        ]
    }
    MOVIE_CHARACTERS = {
        "name": "MOVIE_CHARACTERS",
        "translated_names": {
            "en": 'Movie characters 🎥',
            "ru": 'Персонажи фильмов 🎥'
        },
        f"{UserGender.MALE}_files": [
            {
                'name': '1_IndianaJones.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '2_JamesBond.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '3_HanSolo.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '4_Joker.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '5_Batman.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '6_IronMan.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '7_JackSparrow.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '8_HarryPotter.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '9_JohnWick.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '10_Neo.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '11_SherlockHolmes.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '12_ForrestGump.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '13_FrodoBaggins.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '14_HannibalLecter.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '15_TomasShelbi.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
        ],
        f"{UserGender.FEMALE}_files": [
            {
                'name': '1_Bride.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '2_AmyDunne.png',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '3_AmeliePoulain.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '4_LaraKroft.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '5_Wednesday.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '6_HermioneGranger.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '7_BlackWidow.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '8_WonderWoman.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '9_ElizabethSwann.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '10_Mulan.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '11_HarleyQuinn.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '12_ElizabethBennet.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '13_ClariceStarling.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '14_Trinity.png',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '15_RoseDawson.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
        ]
    }
    PROFESSIONS = {
        "name": "PROFESSIONS",
        "translated_names": {
            "en": 'Professions 🧑‍💻',
            "ru": 'Профессии 🧑‍💻'
        },
        f"{UserGender.MALE}_files": [
            {
                'name': '1_Driver.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '2_Accountant.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '3_Programmer.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '4_Doctor.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '5_Cook.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '6_Seller.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '7_Engineer.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '8_Fitter.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '9_Plumber.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '10_FitnessTrainer.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '11_Astronaut.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '12_Pilot.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '13_RacingPilot.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '14_Detective.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '15_Barista.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
        ],
        f"{UserGender.FEMALE}_files": [
            {
                'name': '1_Driver.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '2_Accountant.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '3_Programmer.png',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '4_Doctor.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '5_Cook.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '6_Seller.jpg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '7_Engineer.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '8_Fitter.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '9_Plumber.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '10_FitnessTrainer.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '11_Astronaut.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '12_Pilot.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '13_RacingPilot.png',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '14_Detective.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
            {
                'name': '15_Barista.jpeg',
                'status': FaceSwapPackageStatus.PUBLIC,
            },
        ]
    }


async def load_face_swap_packages():
    genders = [UserGender.MALE, UserGender.FEMALE]
    packages = [
        FaceSwapPackageInfo.CELEBRITIES['name'],
        FaceSwapPackageInfo.MOVIE_CHARACTERS['name'],
        FaceSwapPackageInfo.PROFESSIONS['name'],
    ]

    for gender in genders:
        for package in packages:
            exists = await get_face_swap_package_by_name_and_gender(package, gender)
            if not exists:
                info = getattr(FaceSwapPackageInfo, package)
                files = info[f'{gender}_files']
                translated_names = info['translated_names']
                await write_face_swap_package(
                    name=package,
                    translated_names=translated_names,
                    gender=gender,
                    files=files,
                    status=FaceSwapPackageStatus.PUBLIC,
                )
