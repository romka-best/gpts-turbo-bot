import asyncio
import logging
import os
import traceback
from typing import Dict, List, Optional

import replicate

from bot.config import config

os.environ["REPLICATE_API_TOKEN"] = config.REPLICATE_API_TOKEN.get_secret_value()
WEBHOOK_REPLICATE_URL = config.WEBHOOK_URL + config.WEBHOOK_REPLICATE_PATH


async def create_face_swap_images(images: List[Dict]):
    tasks = [create_face_swap_image(image['target_image'], image['source_image']) for image in images]
    results = await asyncio.gather(*tasks)

    return results


async def create_face_swap_image(target_image: str, source_image: str) -> Optional[str]:
    try:
        input_parameters = {
            "target_image": target_image,
            "swap_image": source_image,
        }

        model = await replicate.models.async_get("omniedgeio/face-swap")
        version = await model.versions.async_get("c2d783366e8d32e6e82c40682fab6b4c23b9c6eff2692c0cf7585fc16c238cfe")
        prediction = await replicate.predictions.async_create(
            version=version,
            input=input_parameters,
            webhook=WEBHOOK_REPLICATE_URL,
            webhook_events_filter=["completed"],
        )

        return prediction.id
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f'Error in create_face_swap_image: {e}\n{error_trace}')


async def create_music_gen_melody(prompt: str, duration: int) -> Optional[str]:
    try:
        input_parameters = {
            "model_version": "stereo-large",
            "output_format": "mp3",
            "prompt": prompt,
            "duration": duration,
        }

        model = await replicate.models.async_get("meta/musicgen")
        version = await model.versions.async_get("671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb")
        prediction = await replicate.predictions.async_create(
            version=version,
            input=input_parameters,
            webhook=WEBHOOK_REPLICATE_URL,
            webhook_events_filter=["completed"],
        )

        return prediction.id
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f'Error in create_music_gen_melody: {e}\n{error_trace}')
