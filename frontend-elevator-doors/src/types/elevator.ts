export type Call = {
    floor: number
}

export type ElevatorStatus = {
    status: 'parado' | 'subindo' | 'descendo'
    locate: number
    calls: Call[]
}