import type { Door_type } from "../types/door";

const BASE_URL = '/api/doors/'

export async function getDoors(): Promise<Door_type[]> {
    const res = await fetch(`${BASE_URL}/doors/`)
    return res.json()

    // caso não haja backend
    // return [
    //     {localidade: 0, status: 'fechada', statusButton: 'desligado'},
    //     {localidade: 1, status: 'fechada', statusButton: 'ligado'},
    //     {localidade: 2, status: 'fechada', statusButton: 'desligado'},
    // ]
};

export async function pressDoorButton(floor: number) {
    await fetch(
        `${BASE_URL}/doors/button/${floor}`,
        { method: 'POST', }
    )
};