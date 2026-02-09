import { useEffect, useState } from "react";
import { getElevatorStatus } from "./api/elevator";
import { getDoors } from "./api/doors";
import { Elevator } from "./components/Elevator";
import { ElevatorDisplay } from "./components/ElevatorDisplay";
import { Door } from "./components/Door";
import { ElevatorPanel } from "./components/ElevatorPanel";
import './styles/global.css'
import ElevatorButton from "./components/ElevatorButton";

export default function App() {
  const [elevator, setElevator] = useState<any>(null)
  const [doors, setDoors] = useState<any[]>([])
  const panelCalls = new Set<number>();
  const floors = [0, 1, 2, 3, 4, 5, 6, 7];

  useEffect(() => {
    const interval = setInterval(async () => {
      setElevator(await getElevatorStatus())
      setDoors(await getDoors())
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  if (!elevator) return null;

  elevator.calls.forEach((c: any) => {
    if (c.source === 'panel') { panelCalls.add(c.floor) }
  });

  return (
    <div style={{ display: 'flex', gap: 40 }} >
      <Elevator floor={elevator.locate} status={elevator.status} />
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