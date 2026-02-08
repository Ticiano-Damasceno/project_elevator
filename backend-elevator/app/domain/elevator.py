import asyncio
from pydantic import BaseModel
from typing import Literal, List, Optional

Status = Literal['subindo', 'descendo', 'parado']

class ElevatorState(BaseModel):
    status: Status = 'parado'
    localidade: int = 0

class Elevator:
    def __init__(self) -> None:
        self.state = ElevatorState()
        self.calls: List[int] = []
        self.__lock = asyncio.Lock()
        self.__running_task = None
        self.hold_event = asyncio.Event()
        self.hold_event.set()

    def get_status(self) -> dict:
        return {
            'status': self.state.status,
            'locate': self.state.localidade,
            'calls': self.calls
        }

    async def add_call(self, floor: int, source: str) -> None:
        async with self.__lock:
            call = {'floor': floor, 'source': source}
            if floor not in self.calls:
                self.calls.append(call)

    async def remove_call(self, floor: int) -> None:
        async with self.__lock:
            if floor in self.calls:
                self.calls.remove(floor)

    async def up(self):
        if self.state.localidade == 7:
            return
        self.state.status = 'subindo'
        print('subindo para o andar', self.state.localidade + 1)
        await asyncio.sleep(3)
        self.state.localidade += 1
    
    async def down(self):
        if self.state.localidade == 0:
            return
        self.state.status = 'descendo'
        print('descendo para o andar', self.state.localidade - 1)
        await asyncio.sleep(3)
        self.state.localidade -= 1

    def next_floor(self) -> Optional[int]:
        current = self.state.localidade
        upper = sorted(f for f in self.calls if f > current)
        downner = sorted(f for f in self.calls if f < current)
        if not self.calls:
            return None
        if self.state.status == 'subindo' and upper:
            return upper[0]
        elif self.state.status == 'descendo' and downner:
            return downner[0]

        return min(self.calls, key=lambda f: abs(f-current))

    def get_running(self) -> bool:
        return self.__running_task is not None and not self.__running_task.done()

    def set_task(self, task) -> None:
        self.__running_task = task

    def set_status_stop(self) -> None:
        self.state.status = 'parado'
