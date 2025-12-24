import { useState, useEffect } from 'react';

type ElevatorStatus = {
  status: string;
  locate: number;
  calls: number[];
};

const API_URL_ELEVATOR = 'http://localhost:8000';
const floor_list = [0,1,2,3,4,5,6,7];

function App() {
  const [status, setStatus] = useState<ElevatorStatus | null>(null);

  async function loadStatus(): Promise<void> {
    const res = await fetch(`${API_URL_ELEVATOR}/elevator/status`);
    const data: ElevatorStatus = await res.json();
    setStatus(data);
  }

  async function callElevator(floor: number): Promise<void> {
    await fetch(`${API_URL_ELEVATOR}/elevator/call/${floor}`,
      { method: 'POST', }
    );
  };

  useEffect(() => {
    loadStatus();
    const timer = setInterval(loadStatus, 1000);
    return () => clearInterval(timer);
  }, []);

  if (!status) return <p>Loading...</p>

  return (
    <>
      <h2 className="app">Elevador</h2>
      <div className="status">
        <p><b>Status: </b>{status.status}</p>
        <p><b>Andar: </b>{status.locate}</p>
        <p><b>Fila: </b>{status.calls.join(', ') || 'vazia'}</p>
      </div>
      <div className="floors">
        {
          floor_list.map((floor)=>{
            return <button key={floor} onClick={()=>callElevator(floor)} >{floor}</button>
          })
        }
      </div>
    </>
  )
}

export default App
