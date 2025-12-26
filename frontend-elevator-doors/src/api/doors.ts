import type { Door } from "../types/door";

export async function getDoors(): Promise<Door[]> {
    const res = await fetch('http://localhost:3000/doors/')
    return res.json()
    
};

export async function pressDoorButton(floor: number) {
    await fetch(
        `http://localhost:3000/doors/button/${floor}`,
        { method: 'POST', }
    )
};