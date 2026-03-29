import type { ElevatorStatus } from "../types/elevator";

const BASE_URL = '/api/elevator'

export async function getElevatorStatus(): Promise<ElevatorStatus> {
    const res = await fetch(`${BASE_URL}/elevator/status`)
    return res.json()

    // caso não haja backend
    // return {
    //     status: "subindo",
    //     locate: 1,
    //     calls: [],
    // }
};

export async function callElevator(floor: number) {
    await fetch(`${BASE_URL}/elevator/call/${floor}`,
        { method: 'POST' },
    )
};