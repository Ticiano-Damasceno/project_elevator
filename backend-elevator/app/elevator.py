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
        self._lock = asyncio.Lock()
        self.calls: List[int] = []
        self._running = False

    async def add_call(self, floor: int) -> None:
        async with self._lock:
            if floor not in self.calls and floor != self.state.localidade:
                self.calls.append(floor)
            if floor == self.state.localidade and self.state.status == 'parado':
                print('solicita abertura da porta')

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

    def _next_near_floor(self) -> Optional[int]:
        if not self.calls:
            return None
        return min(self.calls, key = lambda x: abs(x - self.state.localidade))

    async def run(self, on_stop_callback):
        if self._running:
            return
        self._running = True
        while self.calls:
            async with self._lock:
                next_floor = self._next_near_floor()
            if next_floor is None:
                break

            if next_floor == self.state.localidade:
                self.calls.remove(next_floor)
                self.state.status = 'parado'
                await on_stop_callback(self.state.localidade)
                continue

            if next_floor > self.state.localidade:
                await self.up()
            elif next_floor < self.state.localidade:
                await self.down()
            if self.state.localidade in self.calls:
                self.calls.remove(self.state.localidade)
                self.state.status = 'parado'
                await on_stop_callback(self.state.localidade)

        self.state.status = 'parado'
        self._running = False
