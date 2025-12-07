import os
import asyncio
import json
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv


from app.elevator import Elevator

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://172.17.144.1:6379")

ELEVATOR_CHANNEL = "elevator:events"
DOORS_COMMAND_CHANNEL = "doors:commands"

app = FastAPI(title = 'Elevator service')
elevator = Elevator()

async def get_redis():
    return redis.from_url(REDIS_URL, decode_responses=True)

async def publish(channel: str, message: dict|str):
    r = await get_redis()
    try:
        if isinstance(message, dict):
            message = json.dumps(message)
        await r.publish(channel, message)
    finally:
        await r.close()

async def on_elevator_stop(floor:int):
    await publish(
        ELEVATOR_CHANNEL,
        {
            'type': 'stop',
            'localidade': floor,
            'status': 'parado'
        }
    )

    await publish(DOORS_COMMAND_CHANNEL, f'open:{floor}')

@app.post('/call/{floor}')
async def call_elevator(floor: int):
    if not 0 <= floor <= 7:
        raise HTTPException(
            status_code=400,
            detail='Andar ser um inteiro entre 0 e 7'
        )
    
    await elevator.add_call(floor)

    await publish(ELEVATOR_CHANNEL, {
        'type': 'queue',
        'calls': elevator.calls
    })

    asyncio.create_task(elevator.run(on_elevator_stop))
    # await elevator.run(on_elevator_stop)

    return JSONResponse({
            'OK': True,
            'fila': elevator.calls,
            'localidade_atual': elevator.state.localidade
    })

@app.get('/status')
async def status():
    return {
        'localidade': elevator.state.localidade,
        'status': elevator.state.status,
        'fila': elevator.calls
    }

@app.websocket('/ws')
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    
    r = await get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(ELEVATOR_CHANNEL)
    
    try:
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, 
                timeout = 1.0
            )
            
            if message:
                await ws.send_text(str(message['data']))
            
            try:
                await asyncio.wait_for(ws.receive_text(), timeout=0.1)
            except asyncio.TimeoutError:
                pass
    
    finally:
        await pubsub.unsubscribe(ELEVATOR_CHANNEL)
        await r.close()
        await ws.close()