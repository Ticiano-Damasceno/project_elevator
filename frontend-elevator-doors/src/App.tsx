import { useEffect, useMemo, useState } from "react";
import { getElevatorStatus } from "./api/elevator";
import { getDoors } from "./api/doors";
import { Elevator } from "./components/Elevator";
import { ElevatorDisplay } from "./components/ElevatorDisplay";
import { ElevatorPanel } from "./components/ElevatorPanel";
import { Door } from "./components/Door";
import './styles/global.css'
import ElevatorButton from "./components/ElevatorButton";
import type { ElevatorStatus } from "./types/elevator";
import type { Door_type } from "./types/door";


export default function App() {
  const [elevator, setElevator] = useState< ElevatorStatus | null >(null);
  const [doors, setDoors] = useState<Door_type[]>([]);
  const panelCalls = useMemo(() => {
    const set = new Set<Number>();
    elevator?.calls.forEach((c:any)=>{
      if (c.source === 'panel') set.add(c.floor);
    });
    return set;
  }, [elevator]);
  const floors = [0, 1, 2, 3, 4, 5, 6, 7];

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        const [elevatorData, doorsData] = await Promise.all([
          getElevatorStatus(),
          getDoors()
        ]);

        if (isMounted){
          setElevator(elevatorData);
          setDoors(doorsData);
        };
      } catch (err) {
        console.error("Erro ao buscar dados", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 1000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  if (!elevator) return null;

  const currentDoor = doors.find(d => d.localidade === elevator.locate);
  console.log(currentDoor);

  return (
    <div style={{ display: 'flex', gap: 40 }} >
      <Elevator floor={elevator.locate} status={elevator.status} doorStatus={currentDoor?.status ?? 'fechada'} />
      <div>
        <ElevatorDisplay
          status={elevator.status}
          locate={elevator.locate}
          calls={elevator.calls}
        />
        <ElevatorPanel>
          {
            floors.map(f => (
              <ElevatorButton
                key={f}
                floor={f}
                status={panelCalls.has(f)}
              />
            ))
          }
        </ElevatorPanel>
      </div>
      <div>
        {
          doors.map(d => (
            <Door
              key={d.localidade}
              floor={d.localidade}
              status={d.status}
              statusButton={d.statusButton}
            />
          ))}
      </div>
    </div>
  )
}