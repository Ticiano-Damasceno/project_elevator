# import json
import asyncio
# from fastapi import Request, FastAPI
from asyncio import create_task

from ...domain.elevator import Elevator
from ...infra.redis.redis_publisher import publish

def get_state(obj: any):
    return obj.app.state if hasattr(obj, "app") else obj.state

async def run_elevator(request: any):
    state = get_state(request)
    elevator: Elevator
    elevator = state.elevator
    redis_client = state.redis_client
    elevator_event_channel = state.ELEVATOR_EVENTS_CHANNEL
    
    if elevator.get_running():
        return {"status": "already running"}

    async def worker():
        while True:
            if not elevator.calls:
                break
            await asyncio.sleep(0.1)
            await elevator.hold_event.wait()
            next_floor = elevator.next_floor()
            if next_floor is None:
                break

            if next_floor > elevator.state.localidade:
                await publish(
                    redis_client,
                    elevator_event_channel,
                    {
                        'type': 'queue',
                        'status': 'subindo',
                        'floor': elevator.state.localidade
                    }
                )
                await elevator.up()
            elif next_floor < elevator.state.localidade:
                await publish(
                    redis_client,
                    elevator_event_channel,
                    {
                        'type': 'queue',
                        'status': 'descendo',
                        'floor': elevator.state.localidade
                    }
                )
                await elevator.down()
            if elevator.state.localidade in elevator.calls:
                await elevator.hold_event.wait()
                await elevator.remove_call(elevator.state.localidade)
                print('Elevador parado no andar', elevator.state.localidade)
                elevator.set_status_stop()
                await publish(
                    redis_client,
                    elevator_event_channel,
                    {
                        'type': 'stop',
                        'status': 'parado',
                        'floor': elevator.state.localidade
                    }
                )
                await publish(
                    redis_client,
                    'doors:commands',
                    {
                        'type': 'open',
                        'floor': elevator.state.localidade
                    }
                )

        
        elevator.set_status_stop()
    
    task = create_task(worker())
    elevator.set_task(task)
    await task
    return {'status': 'started'}