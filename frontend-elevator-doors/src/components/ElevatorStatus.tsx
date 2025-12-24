export default function ElevatorStatus({ status }){
    return (
        <div>
            <p>Status: <b>{status.status}</b></p>
            <p>Andar atual: <b>{status.locate}</b></p>
            <p>Status: {status.call.join(', ')}</p>
        </div>
    );
}