import { callElevator } from "../api/elevator";

type Props = {
    floor: number
    status: boolean
}

const ElevatorButton = ({ floor, status }: Props) => {
    return (
        <button
            key={floor}
            onClick={() => callElevator(floor)}
            className={`${status ? 'ligado' : ''}`}
        >{floor}</button>
    );
}

export default ElevatorButton;