import os
import asyncio
from redis.asyncio import Redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from ..infra.redis.redis_client import create_redis
from ..infra.redis.redis_listener import redis_listener
from ..domain.elevator import Elevator

load_dotenv()

DOORS_EVENTS_CHANNEL = os.getenv('DOORS_EVENTS_CHANNEL')
ELEVATOR_COMMAND_CHANNEL = os.getenv('ELEVATOR_COMMAND_CHANNEL')
ELEVATOR_EVENTS_CHANNEL = os.getenv('ELEVATOR_EVENTS_CHANNEL')

assert DOORS_EVENTS_CHANNEL , 'DOORS_EVENTS_CHANNEL not set'
assert ELEVATOR_COMMAND_CHANNEL , 'ELEVATOR_COMMAND_CHANNEL not set'
assert ELEVATOR_EVENTS_CHANNEL , 'ELEVATOR_EVENTS_CHANNEL not set'
 

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.elevator = Elevator()
    app.state.ELEVATOR_EVENTS_CHANNEL = ELEVATOR_EVENTS_CHANNEL
    app.state.ELEVATOR_COMMAND_CHANNEL = ELEVATOR_COMMAND_CHANNEL
    
    redis_client: Redis
    redis_client = create_redis()
    app.state.redis_client = redis_client

    task_door_event = await redis_listener(app, DOORS_EVENTS_CHANNEL)
    task_elevator_command = await redis_listener(app,ELEVATOR_COMMAND_CHANNEL)

    yield

    task_door_event.cancel()
    task_elevator_command.cancel()

    await asyncio.gather(
        task_door_event,
        task_elevator_command,
        return_exceptions=True
    )

    await redis_client.close()