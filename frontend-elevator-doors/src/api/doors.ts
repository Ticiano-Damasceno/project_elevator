import type { Door } from "../types/door";

const BASE_URL = '/api/doors/'

export async function getDoors(): Promise<Door[]> {
    const res = await fetch(`${BASE_URL}/doors/`)
    return res.json()
    
};

export async function pressDoorButton(floor: number) {
    await fetch(
        `${BASE_URL}/doors/button/${floor}`,
        { method: 'POST', }
    )
};