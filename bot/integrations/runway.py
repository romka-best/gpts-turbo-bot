import asyncio

from runwayml import AsyncRunwayML

from bot.config import config
from bot.database.models.common import RunwayVersion, RunwayResolution, RunwayDuration

client = AsyncRunwayML(
    api_key=config.RUNWAYML_API_TOKEN.get_secret_value(),
)


def get_cost_for_video(duration: RunwayDuration):
    if duration == RunwayDuration.SECONDS_5:
        return 1
    elif duration == RunwayDuration.SECONDS_10:
        return 2

    return 1


async def get_response_video(
    model_version: RunwayVersion,
    prompt_text: str,
    prompt_image: str,
    resolution: RunwayResolution,
    duration: RunwayDuration,
) -> dict:
    response = await client.image_to_video.create(
        model=model_version,
        prompt_text=prompt_text,
        prompt_image=prompt_image,
        ratio=resolution,
        duration=duration,
        watermark=False,
    )

    task_id = response.id

    await asyncio.sleep(10)
    task = await client.tasks.retrieve(task_id)
    for i in range(60):
        await asyncio.sleep(10)
        task = await client.tasks.retrieve(task_id)
        if task.status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break

    return {
        'status': task.status,
        'result': task.output,
        'failure': task.failure,
        'failure_code': task.failure_code,
    }
