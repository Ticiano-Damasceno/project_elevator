import os
import asyncio
import json
import requests
from contextlib import asynccontextmanager
import redis.asyncio as redis
import anyio
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.get_docker_ip import get_docker_ip
from app.verify_redis import check_redis
from app.elevator import Elevator

load_dotenv()
ip = get_docker_ip()
check_redis(ip)
REDIS_URL = os.getenv("REDIS_URL", f"redis://{ip}:6379")

ELEVATOR_CHANNEL = "elevator:events"
ELEVATOR_COMMAND_CHANNEL = "elevator:commands"
DOORS_COMMAND_CHANNEL = "doors:commands"
DOORS_SERVICE_URL = 'http://localhost:3000/doors'

def fetch_doors_state_sync():
    resp = requests.get(DOORS_SERVICE_URL, timeout=5)
    resp.raise_for_status()
    return resp.json()

@asynccontextmanager
async def start(app: FastAPI):
    await load_initial_door_states()
    
    async with anyio.create_task_group() as tg:
        tg.start_soon(elevator_commands)
        tg.start_soon(doors_events_listener)
        yield

app = FastAPI(title = 'Elevator service', lifespan=start)
elevator = Elevator()

door_state: dict[int,str] = {}

async def load_initial_door_states():
    doors = await anyio.to_thread.run_sync(fetch_doors_state_sync)
    print(doors)
    for door in doors:
        door_state[door['localidade']] = door['status']

# async def wait_door_closed(floor: int):
#     try:
#         while door_state.get(floor) != 'fechada':
#             await asyncio.sleep(0.1)
#             print(floor, door_state.get(floor))
#     except asyncio.CancelledError:
#         print('wait_door_closed Cancelled')
#         raise

async def can_elevator_move(floor: int) -> bool:
    return door_state.get(floor) == 'fechada'
    
async def doors_events_listener():
    r = await get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe('doors:events')
    print('Listening on: doors:events')
    
    try:
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0
            )
            
            if message:
                data = json.loads(message['data'])
                floor = data.get('floor')
                event_type = data.get('type')
                if event_type in ('open', 'close'):
                    door_state[floor] = event_type
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print("doors_events cancelled") 
    finally:
        await pubsub.unsubscribe()
        await r.close()

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
    if door_state.get(floor) == 'fechada':
        await publish(
            ELEVATOR_CHANNEL,
            {
                'type': 'stop',
                'localidade': floor,
                'status': 'parado'
            }
        )

        await publish(
            DOORS_COMMAND_CHANNEL, 
            {
                'type': 'open',
                'floor': floor,
                'source': 'elevator'
            }
        )
    else:
        print(f'A porta do andar {floor} está aberta. Aguardar o fechamento...')

async def elevator_commands():
    r = await get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(ELEVATOR_COMMAND_CHANNEL) 
    print('Listening on:', ELEVATOR_COMMAND_CHANNEL)
    
    try:
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0
            )
            
            if message:
                data = json.loads(message['data'])
                print('Messagemm recebida do elevador:', data)
                if data['type'] == 'call':
                    floor = int(data['floor'])
                    if (
                        floor == elevator.state.localidade
                        and elevator.state.status == 'parado'
                    ):
                        asyncio.create_task(open_door_at_current_floor(floor))
                    else:
                        if await can_elevator_move(floor):
                            asyncio.create_task(call_elevator(floor))
                
                
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print("elevator_commands cancelled")       
    finally:
        await pubsub.unsubscribe(ELEVATOR_COMMAND_CHANNEL)
        await r.close()

async def open_door_at_current_floor(floor: int):
    print('Abrindo a porta no andar', floor)
    await publish(
        DOORS_COMMAND_CHANNEL,
        {
            'type': 'open',
            'floor': floor,
            'source': 'elevator'
        }
    )

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

    asyncio.create_task(elevator.run(on_elevator_stop, can_elevator_move))

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