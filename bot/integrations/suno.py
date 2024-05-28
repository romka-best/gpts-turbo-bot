import asyncio
import logging
from typing import List, Dict

import aiohttp
from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage

from bot.config import config
from bot.database.models.generation import GenerationStatus
from bot.database.models.request import RequestStatus
from bot.database.operations.generation.getters import get_generation
from bot.database.operations.generation.updaters import update_generation
from bot.database.operations.request.getters import get_request
from bot.database.operations.request.updaters import update_request
from bot.helpers.handlers.handle_suno_webhook import handle_suno_webhook

SUNO_API_URL = "https://studio-api.suno.ai"
SUNO_TOKEN = config.SUNO_TOKEN.get_secret_value()


class Suno:
    def __init__(self, cookie: str, session: aiohttp.ClientSession = None) -> None:
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "cookie": cookie,
        }
        self.session = session
        self._sid = None

    async def __aenter__(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

        self._sid = await self._get_sid()
        self.songs = Songs(self)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def _get_sid(self) -> str:
        url = "https://clerk.suno.com/v1/client?_clerk_js_version=4.73.2"
        data = await self.request("GET", url)
        return data["response"]["last_active_session_id"]

    async def _get_jwt(self) -> str:
        url = f"https://clerk.suno.com/v1/client/sessions/{self._sid}/tokens/api?_clerk_js_version=4.73.2"
        data = await self.request("POST", url)
        return data["jwt"]

    async def _renew(self) -> None:
        jwt = await self._get_jwt()
        self.headers["Authorization"] = f"Bearer {jwt}"

    async def request(self, method: str, url: str, **kwargs):
        try:
            async with self.session.request(method, url, headers=self.headers, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                await self._renew()
                async with self.session.request(method, url, headers=self.headers, **kwargs) as response:
                    response.raise_for_status()
                    return await response.json()
            raise


class APIResource:
    def __init__(self, client: Suno) -> None:
        self._client = client

    async def request(self, method: str, url: str, **kwargs):
        return await self._client.request(method, url, **kwargs)


class Songs(APIResource):
    async def generate(
        self,
        prompt: str,
        instrumental: bool = False,
        custom: bool = False,
        tags: str = ""
    ) -> List:
        url = f"{SUNO_API_URL}/api/generate/v2/"
        payload = {
            "mv": "chirp-v3-5",
            "prompt": prompt if custom else "",
            "gpt_description_prompt": "" if custom else prompt,
            "make_instrumental": instrumental,
            "tags": tags if custom else "",
        }
        data = await self.request("POST", url, json=payload)
        return data["clips"]

    async def get(self, id: str) -> Dict:
        url = f"{SUNO_API_URL}/api/feed/?ids={id}"
        data = await self.request("GET", url)
        return data[0]


async def generate_song(
    prompt: str,
    instrumental: bool = False,
    custom: bool = False,
    tags: str = ""
) -> List[str]:
    async with Suno(cookie=SUNO_TOKEN) as client:
        clips = await client.songs.generate(
            prompt=prompt,
            instrumental=instrumental,
            custom=custom,
            tags=tags,
        )
        ids = []
        for clip in clips:
            ids.append(clip.get('id'))

        return ids


async def check_song(bot: Bot, storage: BaseStorage, song_id: str):
    async with aiohttp.ClientSession() as session:
        async with Suno(cookie=SUNO_TOKEN, session=session) as client:
            need_to_reset = True
            for i in range(10):
                try:
                    clip = await client.songs.get(id=song_id)
                    status = clip.get('status')
                    if status == 'complete' and not clip.get('is_video_pending'):
                        await handle_suno_webhook(bot, storage, clip)
                        need_to_reset = False
                        break
                    elif status == 'error':
                        await handle_suno_webhook(bot, storage, clip)
                        need_to_reset = False
                        break
                    else:
                        await asyncio.sleep(60)
                except Exception as e:
                    logging.error(f'Error in check_song: {e}')
                    break
            if need_to_reset:
                generation = await get_generation(song_id)
                await update_generation(generation.id, {
                    "status": GenerationStatus.FINISHED,
                    "has_error": True,
                })

                request = await get_request(generation.request_id)
                await update_request(request.id, {
                    "status": RequestStatus.FINISHED
                })


async def get_song(song_id: str, session):
    async with Suno(cookie=SUNO_TOKEN, session=session) as client:
        clip = await client.songs.get(id=song_id)

        return clip
