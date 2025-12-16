import redis.asyncio as redis
from .verify_redis import check_redis
from ...utils.get_docker_ip import get_docker_ip


def create_redis() -> redis.Redis:
    ip = get_docker_ip()

    if not check_redis(ip):
        raise RuntimeError('Redis está offline.')

    return redis.Redis(host = ip, port = 6379, decode_responses=True)