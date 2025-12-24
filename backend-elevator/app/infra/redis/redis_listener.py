import json
import asyncio
from fastapi import FastAPI
from ...application.handlers.handler_redis_message import handler_redis_message

async def redis_listener(app: FastAPI, channel: str):
    redis = app.state.redis_client
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    
    async def listen():
        try:
            while True:
                msg = await pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout = 1.0
                )
                if msg:
                    data = json.loads(msg['data'])
                    channel_name = msg['channel']
                    if isinstance(channel_name, bytes):
                        channel_name = channel_name.decode()
                    try:
                        await handler_redis_message(app,data, channel_name)
                    except Exception as e:
                        print('Redis_listener error:', e)
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            await pubsub.unsubscribe(channel)
            await pubsub.close()
            raise

    return asyncio.create_task(listen())
