import asyncio
from fastapi import FastAPI
from ...domain.elevator import Elevator

async def handler_redis_message(app:FastAPI, data: dict, channel: str):
    elevator: Elevator = app.state.elevator
    print(data)
    if data.get('source') == 'door':
        if data.get('type') == 'call':
            floor = data.get('floor')
            print('Recebido solicitação da porta:', data)
            await elevator.call(floor, 'door')
        else:
            print('Recebido solicitação da porta:', data)
            if data.get('type') == 'aberta':
                elevator.pause()
            elif data.get('type') == 'fechada':
                elevator.resume()
