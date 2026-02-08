export type ElevatorStatus = {
    status: 'parado' | 'subindo' | 'descendo'
    locate: number
    calls: object[]
}