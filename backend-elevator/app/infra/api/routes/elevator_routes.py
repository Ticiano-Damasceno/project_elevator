from fastapi import APIRouter, Request, HTTPException, status

router = APIRouter(tags=['Elevator'])

@router.get('/status')
async def get_status(request: Request):
    elevator = request.app.state.elevator
    return elevator.get_status()

@router.post('/call/{floor}', status_code=status.HTTP_202_ACCEPTED)
async def call_elevator(floor: int, request: Request):
    if floor < 0 or floor > 7:
        raise HTTPException(
            status_code=400, 
            detail='Andar inválido!'
        )
    
    elevator = request.app.state.elevator
    await elevator.call(floor, 'panel')
    
    return {
            'OK': True,
            'floor_called': floor
    }
