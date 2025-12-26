import { useEffect, useState } from "react";
import { getElevatorStatus } from "./api/elevator";
import { getDoors } from "./api/doors";
import { Elevator } from "./components/Elevator";
import { Door } from "./components/Door";
import { ElevatorPanel } from "./components/ElevatorPanel";
import './styles/global.css'

export default function App() {
  const [elevator, setElevator] = useState<any>(null)
  const [doors, setDoors] = useState<any[]>([])

  useEffect(() =>{
    const interval = setInterval(async () => {
      setElevator(await getElevatorStatus())
      setDoors(await getDoors())
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  if (!elevator) return null

  return (
    <div style={{ display: 'flex', gap: 40 }} >
      <Elevator floor={elevator.locate} status={elevator.status} />
      <ElevatorPanel floors={[0,1,2,3,4,5,6,7]} />
      <div>
        {doors.map(d => (
          <Door
            key = {d.localidade}
            floor = {d.localidade}
            status = {d.status}
          />
        ))}
      </div>
    </div>
  )
}