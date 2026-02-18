import '../styles/Elevator.css'
import type { ElevatorStatus } from '../types/elevator'

type Props = {
  floor: number
  status: ElevatorStatus['status']
}

const TOTAL_FLOORS = 8
const SHAFT_HEIGHT = 480
const CABIN_HEIGHT = 60
const MAX_BOTTOM = SHAFT_HEIGHT - CABIN_HEIGHT


export function Elevator({ floor }: Props) {
    const position = (floor/(TOTAL_FLOORS-1) * MAX_BOTTOM)
    return (
        <div className="elevator-shaft">
            <div
                className="elevator-box"
                style={{ bottom: `${position}px` }}
            >
                <div className="display" style={{ color: 'white' }}>
                    {floor}
                </div>
            </div>
        </div>
    );
}