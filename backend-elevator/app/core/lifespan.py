import os
import asyncio
from redis.asyncio import Redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from ..infra.redis.redis_client import create_redis
from ..infra.redis.redis_listener import redis_listener
from ..infra.redis.redis_publisher import publish
from ..domain.elevator import Elevator

load_dotenv()

host = os.getenv("REDIS_HOST", "localhost")
port = int(os.getenv("REDIS_PORT", 6379))

DOORS_EVENTS_CHANNEL = os.getenv('DOORS_EVENTS_CHANNEL', 'doors:events')
DOORS_COMMAND_CHANNEL = os.getenv('DOORS_COMMAND_CHANNEL', 'doors:commands')
ELEVATOR_COMMAND_CHANNEL = os.getenv('ELEVATOR_COMMAND_CHANNEL', 'elevator:commands')
ELEVATOR_EVENTS_CHANNEL = os.getenv('ELEVATOR_EVENTS_CHANNEL', 'elevator:events')

assert DOORS_EVENTS_CHANNEL , 'DOORS_EVENTS_CHANNEL not set'
assert DOORS_COMMAND_CHANNEL , 'DOORS_COMMAND_CHANNEL not set'
assert ELEVATOR_COMMAND_CHANNEL , 'ELEVATOR_COMMAND_CHANNEL not set'
assert ELEVATOR_EVENTS_CHANNEL , 'ELEVATOR_EVENTS_CHANNEL not set'
 

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    redis_client: Redis
    redis_client = create_redis(host, port)
    app.state.redis_client = redis_client

    async def elevator_publisher(event: dict):
        await publish(
            redis_client=redis_client,
            channel=ELEVATOR_EVENTS_CHANNEL,
            data=event
        )
    async def door_publisher(event: dict):
        await publish(
            redis_client=redis_client,
            channel=DOORS_COMMAND_CHANNEL,
            data=event
        )
    
    app.state.elevator = Elevator(publisher=elevator_publisher, door_publisher=door_publisher)
    app.state.ELEVATOR_EVENTS_CHANNEL = ELEVATOR_EVENTS_CHANNEL
    app.state.ELEVATOR_COMMAND_CHANNEL = ELEVATOR_COMMAND_CHANNEL
    
    

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