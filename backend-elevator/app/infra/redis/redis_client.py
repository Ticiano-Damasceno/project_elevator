import redis.asyncio as redis

def create_redis(host: str, port: int) -> redis.Redis:
    return redis.Redis(
        host = host, 
        port = port, 
        decode_responses=True
    )