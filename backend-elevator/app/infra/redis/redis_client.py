import redis.asyncio as redis

from .verify_redis import check_redis
from ...utils.get_docker_ip import get_docker_ip

ip = get_docker_ip()

def create_redis():
    if check_redis(ip):
        return redis.Redis(host = ip, port = 6379)