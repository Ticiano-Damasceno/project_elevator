import type { ElevatorStatus } from "../types/elevator";
import '../styles/ElevatorDisplay.css'


export function ElevatorDisplay({ status, locate, calls }: ElevatorStatus) {
    const uniqueFloors = [...new Set(calls.map(c => c.floor))];
    return (
        <div className="display-lista">
            <div className="display-status">
                <strong>{status}</strong>
                <div className="locate">{locate}</div>
            </div>
            <div className="lista">
                {uniqueFloors}
            </div>
        </div>
    )
}