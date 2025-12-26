import { callElevator } from "../api/elevator";
import '../styles/ElevatorPanel.css'

type Props = {
    floors: number[]
}

export function ElevatorPanel({ floors }: Props) {
    return (
        <div className="panel">
            {floors.map (f => (
                <button key={f} onClick={() => callElevator(f)} >{f}</button>
            ))}
        </div>
    )
}