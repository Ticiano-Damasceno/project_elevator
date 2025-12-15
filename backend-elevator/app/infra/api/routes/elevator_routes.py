import asyncio
from fastapi import APIRouter, Request
router = APIRouter(prefix='/elevator')

@router.get('/status')
async def get_stats(request: Request):
    elevator = request.app.state.elevator
    return elevator.get_status()

@router.post('/call/{floor}')
async def call_elevator(floor: int, request: Request):
    elevator = request.app.state.elevator
    await elevator.add_call(floor)
    
    if not elevator._running:
        async def on_stop(floor: int):
            print('Parado no andar', floor)
    
        asyncio.create_task(
            elevator.run(on_stop, True)
        )
        