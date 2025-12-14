import { Injectable, OnModuleInit } from '@nestjs/common';
import { RedisService } from '../redis/redis.service';
import { RedisProvider } from 'src/redis/redis.provider';

export type DoorStatus = 'transição' | 'aberta' | 'fechada';

export interface DoorState {
    localidade: number;
    status: DoorStatus;
}

@Injectable()
export class DoorsService implements OnModuleInit {
    private doors: DoorState[] = [];

    constructor(private redisService: RedisService, private redis: RedisProvider){
        for (let i=0;i<=7;i++){
            this.doors.push({
                localidade: i,
                status: 'fechada',
            });
        }
    };

    async onModuleInit() {
        const redis = this.redisService.getClient();
        redis.subscribe('doors:commands', (message: any) => {
            console.log('Mensagem recebida do elevador:', message);
            this.handleElevatorCommand(message);
        });
    }

    private async handleElevatorCommand(message: string) {
        let data: any;
        try {
            data = JSON.parse(message);
        } catch (err) {
            console.log('JSON inválido:', message);
            return;
        }
        const { type, floor, } = data;
        if(typeof floor !== 'number'){
            console.log('Andar inválido recebido:', data);
            return;
        }
        switch(type){
            case 'open':
                await this.openCloseDoor(floor);
                break;
            case 'close':
                await this.closeDoor(floor);
                break;
        }
    }

    getAllDoors(){
        return this.doors;
    }

    getDoorState(floor:number){
        return this.doors[floor];
    }

    private wait(ms:number){
        return new Promise(resolve => setTimeout(resolve,ms));
    }

    async emitElevatorCall(floor: number){
        await this.redis.publish(
            'elevator:commands',
            {
                type: 'call',
                floor,
                source: 'door',
            }
        );
    }

    async pressButton(floor: number){
        console.log(`Button pressed at floor ${floor}. Calling elevator...`);
        await this.emitElevatorCall(floor);
    }

    async openDoor(floor:number){
        const door = this.doors[floor];
        if(!door) return;
        if (door.status === 'aberta' || door.status === 'transição') return;
        console.log(`Porta ${floor}: iniciando abertura...`);
        door.status = 'transição';
        await this.wait(2000);
        door.status = 'aberta';
        console.log(`Porta ${floor}: aberta.`);
        await this.redis.publish(
            'doors:events',
            {
                type: 'aberta',
                floor,
                source: 'door'
            }
        );
    }

    async closeDoor(floor:number){
        const door = this.doors[floor];
        if(!door) return;
        if (door.status === 'fechada' || door.status === 'transição') return;
        console.log(`Porta ${floor}: iniciando fechamento...`);
        door.status = 'transição';
        await this.wait(2000);
        door.status = 'fechada';
        console.log(`Porta ${floor}: fechada.`);
        await this.redis.publish(
            'doors:events',
            {
                type: 'fechada',
                floor,
                source: 'door'
            }
        )
    }

    async openCloseDoor(floor:number){
        const door = this.doors[floor];
        if(!door) return;

        switch(door.status){
            case 'aberta':
                return this.closeDoor(floor);
            case 'fechada':
                await this.openDoor(floor);
                await this.wait(6000);
                return this.closeDoor(floor);
            case 'transição':
                console.log(`Porta ${floor} em transição. Comando ignorado.`)
                return;
        }

    }

}
