import '../styles/ElevatorDoor.css';

type Props = {
    status: 'aberta' | 'fechada'
}

const ElevatorDoor = ({ status }:Props) => {
    const isOpen = status !== 'fechada';
    return ( 
        <div className="door-container">
            <div className={`door-panel left ${isOpen ? 'open' : ''}`} />
            <div className={`door-panel right ${isOpen ? 'open' : ''}`} />
        </div>
    );
}
 
export default ElevatorDoor;