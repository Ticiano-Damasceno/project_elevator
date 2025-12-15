
from redis.asyncio.client import Redis
import json

async def redis_listener(redis_client: Redis, channel: str):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    
    async for msg in pubsub.listen():
        if msg['type'] == 'message':
            data = json.loads(msg['data'])
            print(f'Mensagem recebida do {channel}:',data)