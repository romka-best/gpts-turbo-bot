import asyncio
import logging
import os
import time
import traceback
from typing import Dict, List

import replicate

from bot.config import config

os.environ["REPLICATE_API_TOKEN"] = config.REPLICATE_API_TOKEN.get_secret_value()
FACE_SWAP_MODEL_REF = "yan-ops/face_swap:d5900f9ebed33e7ae08a07f17e0d98b4ebc68ab9528a70462afc3899cfe23bab"


async def get_face_swap_images(images: List[Dict]):
    tasks = [get_face_swap_image(image['target_image'], image['source_image']) for image in images]
    results = await asyncio.gather(*tasks)

    return results


async def get_face_swap_image(target_image: str, source_image: str) -> Dict:
    try:
        input_parameters = {
            "target_image": target_image,
            "source_image": source_image,
        }

        start_time = time.time()
        output = await replicate.async_run(
            ref=FACE_SWAP_MODEL_REF,
            input=input_parameters
        )

        end_time = time.time()
        seconds = end_time - start_time

        return {
            "image": output['image'],
            "seconds": seconds,
        }
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f'Произошла ошибка при обращении к ReplicateAPI: {e}\n{error_trace}')
        return {
            "image": None,
            "seconds": 0,
        }
