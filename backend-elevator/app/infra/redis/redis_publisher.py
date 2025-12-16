import json
from typing import Any
from redis.asyncio.client import Redis

async def publish(redis_client: Redis, channel: str, data: Any):
    if not redis_client:
        return
    await redis_client.publish(channel,json.dumps(data))