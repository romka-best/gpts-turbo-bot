import asyncio
import logging
import os
import traceback
from typing import Dict, List, Optional

import replicate

from bot.config import config

os.environ["REPLICATE_API_TOKEN"] = config.REPLICATE_API_TOKEN.get_secret_value()
FACE_SWAP_MODEL_REF = "yan-ops/face_swap:d5900f9ebed33e7ae08a07f17e0d98b4ebc68ab9528a70462afc3899cfe23bab"
WEBHOOK_REPLICATE_URL = config.WEBHOOK_URL + config.WEBHOOK_REPLICATE_PATH


async def create_face_swap_images(images: List[Dict]):
    tasks = [create_face_swap_image(image['target_image'], image['source_image']) for image in images]
    results = await asyncio.gather(*tasks)

    return results


async def create_face_swap_image(target_image: str, source_image: str) -> Optional[str]:
    try:
        input_parameters = {
            "target_image": target_image,
            "source_image": source_image,
            "cache_days": 180,
        }

        model = await replicate.models.async_get("yan-ops/face_swap")
        version = await model.versions.async_get("d5900f9ebed33e7ae08a07f17e0d98b4ebc68ab9528a70462afc3899cfe23bab")
        prediction = await replicate.predictions.async_create(
            version=version,
            input=input_parameters,
            webhook=WEBHOOK_REPLICATE_URL,
            webhook_events_filter=["completed"]
        )

        return prediction.id
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f'Произошла ошибка при обращении к ReplicateAPI: {e}\n{error_trace}')
