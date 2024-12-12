import asyncio
import os
from typing import Optional

import replicate

from bot.config import config
from bot.database.models.common import PhotoshopAIAction, AspectRatio

os.environ['REPLICATE_API_TOKEN'] = config.REPLICATE_API_TOKEN.get_secret_value()
WEBHOOK_REPLICATE_URL = config.WEBHOOK_URL + config.WEBHOOK_REPLICATE_PATH


async def create_face_swap_images(images: list[dict]):
    tasks = [create_face_swap_image(image['target_image'], image['source_image']) for image in images]
    results = await asyncio.gather(*tasks)

    return results


async def create_face_swap_image(target_image: str, source_image: str) -> Optional[str]:
    input_parameters = {
        'input_image': target_image,
        'swap_image': source_image,
    }

    model = await replicate.models.async_get('codeplugtech/face-swap')
    version = await model.versions.async_get('278a81e7ebb22db98bcba54de985d22cc1abeead2754eb1f2af717247be69b34')
    prediction = await replicate.predictions.async_create(
        version=version,
        input=input_parameters,
        webhook=WEBHOOK_REPLICATE_URL,
        webhook_events_filter=['completed'],
    )

    return prediction.id


async def create_photoshop_ai_image(action: PhotoshopAIAction, image_url: str) -> Optional[str]:
    if action == PhotoshopAIAction.RESTORATION:
        input_parameters = {
            'img': image_url,
        }

        model = await replicate.models.async_get('tencentarc/gfpgan')
        version = await model.versions.async_get('0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c')
    elif action == PhotoshopAIAction.COLORIZATION:
        input_parameters = {
            'image': image_url,
        }

        model = await replicate.models.async_get('cjwbw/bigcolor')
        version = await model.versions.async_get('9451bfbf652b21a9bccc741e5c7046540faa5586cfa3aa45abc7dbb46151a4f7')
    elif action == PhotoshopAIAction.REMOVAL_BACKGROUND:
        input_parameters = {
            'image': image_url,
        }

        model = await replicate.models.async_get('cjwbw/rembg')
        version = await model.versions.async_get('fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003')
    else:
        return

    prediction = await replicate.predictions.async_create(
        version=version,
        input=input_parameters,
        webhook=WEBHOOK_REPLICATE_URL,
        webhook_events_filter=['completed'],
    )

    return prediction.id


async def create_music_gen_melody(prompt: str, duration: int) -> Optional[str]:
    input_parameters = {
        'model_version': 'stereo-large',
        'output_format': 'mp3',
        'prompt': prompt,
        'duration': duration,
    }

    model = await replicate.models.async_get('meta/musicgen')
    version = await model.versions.async_get('671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb')
    prediction = await replicate.predictions.async_create(
        version=version,
        input=input_parameters,
        webhook=WEBHOOK_REPLICATE_URL,
        webhook_events_filter=['completed'],
    )

    return prediction.id


async def create_stable_diffusion_image(
    prompt: str,
    aspect_ratio: AspectRatio,
    image_link: Optional[str] = None,
) -> Optional[str]:
    input_parameters = {
        'prompt': prompt,
        'output_format': 'png',
        'output_quality': 100,
        'aspect_ratio': aspect_ratio,
    }
    if image_link:
        input_parameters['image'] = image_link
        input_parameters['prompt_strength'] = 0.75

    model = await replicate.models.async_get('stability-ai/stable-diffusion-3.5-large-turbo')
    prediction = await replicate.predictions.async_create(
        model=model,
        input=input_parameters,
        webhook=WEBHOOK_REPLICATE_URL,
        webhook_events_filter=['completed'],
    )

    return prediction.id


async def create_flux_image(
    prompt: str,
    aspect_ratio: AspectRatio,
    safety_tolerance=3,
    image_link: Optional[str] = None,
) -> Optional[str]:
    input_parameters = {
        'prompt': prompt,
        'output_format': 'jpg',
        'output_quality': 100,
        'aspect_ratio': aspect_ratio,
        'safety_tolerance': safety_tolerance,
    }
    if image_link:
        input_parameters['image_prompt'] = image_link

    model = await replicate.models.async_get('black-forest-labs/flux-1.1-pro')
    prediction = await replicate.predictions.async_create(
        model=model,
        input=input_parameters,
        webhook=WEBHOOK_REPLICATE_URL,
        webhook_events_filter=['completed'],
    )

    return prediction.id
