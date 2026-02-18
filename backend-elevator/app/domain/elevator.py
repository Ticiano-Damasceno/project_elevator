import asyncio
from pydantic import BaseModel
from typing import Literal, List, Optional, Callable, Awaitable, Dict

CallSource = Literal['door', 'panel']
Status = Literal['subindo', 'descendo', 'parado']

class ElevatorState(BaseModel):
    status: Status = 'parado'
    localidade: int = 0

class Elevator:
    def __init__(
            self,
            publisher: Optional[Callable[[dict], Awaitable[None]]] = None,
            door_publisher: Optional[Callable[[dict], Awaitable[None]]] = None
        ) -> None:
        self.state = ElevatorState()
        self.calls: List[dict] = []
        self.__lock = asyncio.Lock()
        self.__task: asyncio.Task | None = None
        self.call_event = asyncio.Event()
        self.hold_event = asyncio.Event()
        self.hold_event.set()
        self.publisher = publisher
        self.door_publisher = door_publisher
        self.__task = asyncio.create_task(self._worker())
        self.__next_floor: Optional[int] = None

    def get_status(self) -> dict:
        return {
            'status': self.state.status,
            'locate': self.state.localidade,
            'calls': self.calls
        }

    def _call_exists(self, floor: int, source: CallSource) -> bool:
        return any(
            c['floor'] == floor and c['source'] == source for c in self.calls
        )

    async def call(self, floor: int, source: CallSource) -> bool:
        async with self.__lock:
            if self._call_exists(floor, source):
                return False
            
            self.calls.append({'floor':floor, 'source':source})
            self.call_event.set()
            return True

    def pause(self):
        print('Elevador parado - Porta Aberta')
        self.hold_event.clear()

    def resume(self):
        print('Elevador continuado - Porta Fechada')
        self.hold_event.set()

    def is_running(self) -> bool:
        return self.__task is not None and not self.__task.done()

    async def _worker(self):
        while True:
            await self.call_event.wait()
            self.call_event.clear()

            while self.calls:
                self.__next_floor = self.next_floor()
                if self.__next_floor is None:
                    self.state.status = 'parado'
                    break
                
                await self.hold_event.wait()
                if self.__next_floor > self.state.localidade:
                    self.state.status = 'subindo'
                    await self._publish('queue')
                    await self.up()

                elif self.__next_floor < self.state.localidade:
                    self.state.status = 'descendo'
                    await self._publish('queue')
                    await self.down()

                if self.__next_floor == self.state.localidade:
                    # self.state.status = 'parado'
                    self.hold_event.clear()
                    print('Parado no andar', self.state.localidade)
                    await self._publish('stop')
                    await self._publish_door()

                    await self.hold_event.wait()
                    self.remove_call_at_floor(self.state.localidade)
    
    async def _publish(self, type_:str):
        if self.publisher:
            await self.publisher({
                'type': type_,
                'status': self.state.status,
                'floor': self.state.localidade
            })

    async def _publish_door(self):
        if self.door_publisher:
            await self.door_publisher({
                'type': 'open',
                'floor': self.state.localidade
            })

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
        if not self.calls:
            return None
    
        if self.state.status == 'parado':
            
            return min(
                (c['floor'] for c in self.calls),
                key = lambda f: abs(f - self.state.localidade)
            )
            
        elif self.state.status == 'subindo':
            return self._next_subindo()

        elif self.state.status == 'descendo':
            return self._next_descendo()
        
        return None
    
    def _split_calls(self):
        current = self.state.localidade

        acima_panel = []
        acima_door = []
        abaixo = []

        for c in self.calls:
            if c['floor'] > current:
                if c['source'] == 'panel':
                    acima_panel.append(c['floor'])
                else:
                    acima_door.append(c['floor'])
            elif c['floor'] < current:
                abaixo.append(c['floor'])

        return acima_panel, acima_door, abaixo

    def _next_subindo(self):
        acima_panel, acima_door, _ = self._split_calls()

        if acima_panel:
            if min(acima_panel) == self.state.localidade:
                return self.__next_floor
            return min(acima_panel)        # crescente
        if acima_door:
            return max(acima_door)        # door em ordem decrescente

        return None

    def _next_descendo(self):
        _, _, abaixo = self._split_calls()

        if abaixo:
            if max(abaixo) == self.state.localidade:
                return self.__next_floor
            return max(abaixo)            # decrescente

        return None


    def remove_call_at_floor(self, floor: int) -> None:
        self.calls = [c for c in self.calls if c['floor'] != floor]