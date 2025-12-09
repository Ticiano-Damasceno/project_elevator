import { Injectable, OnModuleInit } from '@nestjs/common';
import { RedisService } from '../redis/redis.service';

export type DoorStatus = 'transição' | 'aberta' | 'fechada';

export interface DoorState {
    localidade: number;
    status: DoorStatus;
}

@Injectable()
export class DoorsService implements OnModuleInit {
    private doors: DoorState[] = [];

    constructor(private redisService: RedisService){
        for (let i=0;i<=7;i++){
            this.doors.push({
                localidade: i,
                status: 'fechada',
            });
        }
    };

    async onModuleInit() {
        const redis = this.redisService.getClient();

        await redis.subscribe('doors:commands', async (message) => {
            console.log('Mensagem recebida do elevador:', message);

            const [command, floorStr] = message.split(':');
            const floor = Number(floorStr);
            
            if(command === 'open'){
                console.log(`Abrindo porta do andar ${floor} por comando elevador...`);
                await this.openCloseDoor(floor);
            }
        });

        console.log('Backend-doors inscrito no canal doors:commands');
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

    async openDoor(floor:number){
        const door = this.doors[floor];
        if(!door) return;
        if (door.status === 'aberta' || door.status === 'transição') return;
        console.log(`Porta ${floor}: iniciando abertura...`);
        door.status = 'transição';
        await this.wait(2000);
        door.status = 'aberta';
        console.log(`Porta ${floor}: aberta.`);
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
