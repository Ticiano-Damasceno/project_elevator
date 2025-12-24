import json
import asyncio
from fastapi import FastAPI
from .handler_elevator import run_elevator
from ...domain.elevator import Elevator
from ...infra.redis.redis_publisher import publish

async def handler_redis_message(app:FastAPI, data: dict, channel: str):
    elevator: Elevator
    elevator = app.state.elevator
    redis_client = app.state.redis_client

    if data.get('type') == 'call':
        floor = data.get('floor')
        print('Recebido solicitação da porta:', data)
        if floor not in elevator.calls:
            await elevator.add_call(floor)
            print(elevator.calls)
            if not elevator.get_running():
                asyncio.create_task(run_elevator(app))

        await publish(
            redis_client,
            channel,
            {
                'type': channel,
                'status': elevator.state.status,
                'floor': elevator.state.localidade
            }
        )
    if data.get('source') == 'door':
        if data.get('type') == 'aberta':
            elevator.hold_event.clear()
            print('porta aberta')
        elif data.get('type') == 'fechada':
            elevator.hold_event.set()
            print('porta fechada')
    