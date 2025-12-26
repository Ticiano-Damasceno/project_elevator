import type { ElevatorStatus } from "../types/elevator";

export async function getElevatorStatus(): Promise<ElevatorStatus> {
    const res = await fetch('http://localhost:8000/elevator/status')
    return res.json()
};

export async function callElevator(floor: number) {
    await fetch(`http://localhost:8000/elevator/call/${floor}`,
        { method: 'POST' },
    )
};