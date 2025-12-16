import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from ....application.handlers.handler_elevator import run_elevator

router = APIRouter(prefix='/elevator')

@router.get('/status')
async def get_stats(request: Request):
    elevator = request.app.state.elevator
    return elevator.get_status()

@router.post('/call/{floor}')
async def call_elevator(floor: int, request: Request):
    if floor < 0 or floor > 7:
        return JSONResponse(status_code=400, content={'error': 'Andar inválido!'})
    
    elevator = request.app.state.elevator
    await elevator.add_call(floor)
    
    if not elevator.get_running():
        asyncio.create_task(run_elevator(request))
    
    return {
            'OK': True,
            'fila': elevator.calls,
            'localidade_atual': elevator.state.localidade
    }
