import { pressDoorButton } from "../api/doors";
import '../styles/Door.css';

type Props = {
    floor: number
    status: string
    statusButton: string
}

export function Door({floor, status, statusButton}: Props){
    const isOpen = status !== 'fechada';
    const isCalling = statusButton === 'ligado';
    return (
        <div className={`door ${isOpen ? 'open': ''}`}>
            <strong style={{ color: '#e6f0ff' }} >Floor {floor}</strong>
            <div className="door-status">{status}</div>
            <button className={`door-button ${isCalling ? 'ligado': ''}`} onClick={() => pressDoorButton(floor)} >Chamar</button>
        </div>
    )
}