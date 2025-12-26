import { pressDoorButton } from "../api/doors";
import '../styles/Door.css';

type Props = {
    floor: number
    status: string
}

export function Door({floor, status}: Props){
    const isOpen = status === 'aberta'
    return (
        <div className={`door ${isOpen ? 'open': ''}`}>
            <strong style={{ color: 'white' }} >Floor {floor}</strong>
            <div className="door-status">Porta {status}</div>
            <button onClick={() => pressDoorButton(floor)} >Chamar</button>
        </div>
    )
}