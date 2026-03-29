import '../styles/Elevator.css'
import type { Door_type } from '../types/door'
import type { ElevatorStatus } from '../types/elevator'
import ElevatorDoor from './ElevatorDoor'

type Props = {
  floor: number
  status: ElevatorStatus['status']
  doorStatus: Door_type['status']
}

const TOTAL_FLOORS = 8
const SHAFT_HEIGHT = 480
const CABIN_HEIGHT = 60
const MAX_BOTTOM = SHAFT_HEIGHT - CABIN_HEIGHT


export function Elevator({ floor, doorStatus }: Props) {
    const position = (floor/(TOTAL_FLOORS-1) * MAX_BOTTOM)
    return (
        <div className="elevator-shaft">
            <div
                className={`elevator-box ${status}`}
                style={{ bottom: `${position}px` }}
            >
                <ElevatorDoor status={doorStatus ?? 'fechada'} />
            </div>
        </div>
    );
}