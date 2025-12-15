import os
import asyncio
from redis import Redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from ..infra.redis.redis_client import create_redis
from ..infra.redis.redis_listener import redis_listener
from ..domain.elevator import Elevator

load_dotenv()

DOORS_EVENTS_CHANNEL = os.getenv('DOORS_EVENTS_CHANNEL')
ELEVATOR_COMMAND_CHANNEL = os.getenv('ELEVATOR_COMMAND_CHANNEL')

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.elevator = Elevator()
    redis_client: Redis
    redis_client = create_redis()
    task_door_event = asyncio.create_task(
        redis_listener(
            redis_client, 
            DOORS_EVENTS_CHANNEL
        )
    )
    task_elevator_command = asyncio.create_task(
        redis_listener(
            redis_client, 
            ELEVATOR_COMMAND_CHANNEL
        )
    )
    yield
    task_door_event.cancel()
    task_elevator_command.cancel()
    await redis_client.close()

