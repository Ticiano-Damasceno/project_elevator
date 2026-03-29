import type { ElevatorStatus } from "../types/elevator";
import '../styles/ElevatorDisplay.css'


export function ElevatorDisplay({ status, locate, calls }: ElevatorStatus) {
    const uniqueFloors = [...new Set(calls.map(c => c.floor))];
    const getDirection = () => {
        if (status === 'subindo') return '▲';
        if (status === 'descendo') return '▼';
        return '■';  
    };
    return (
        <div className="display-lista">
            <div className="display-status">
                <strong>{getDirection()}</strong>
                <div className="locate">{locate}</div>
            </div>
            <div className="lista">
                {uniqueFloors.join(', ')}
            </div>
        </div>
    )
}