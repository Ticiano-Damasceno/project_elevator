import type { ElevatorStatus } from "../types/elevator";
import '../styles/ElevatorDisplay.css'

export function ElevatorDisplay({status, locate, calls}: ElevatorStatus){
    return (
        <div className="display-lista">
            <div className="display-status">
                <strong>{status }</strong>
                <div className="locate">{locate}</div>
            </div>
            <div className="lista">
                {calls}
            </div>
        </div>
    )
}