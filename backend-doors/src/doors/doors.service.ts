import { Injectable, OnModuleInit } from '@nestjs/common';
import { RedisService } from '../redis/redis.service';
import { RedisProvider } from 'src/redis/redis.provider';
import { Redis } from 'ioredis';
import { getDokcerIp } from '../utils/getDockerIp';

export type DoorStatus = 'transição' | 'aberta' | 'fechada';

export interface DoorState {
    localidade: number;
    status: DoorStatus;
}

@Injectable()
export class DoorsService implements OnModuleInit {
    private doors: DoorState[] = [];
    private redisPub: Redis;
    private redisSub: Redis;
    private ip: string;

    constructor(private redisService: RedisService, private redis: RedisProvider){
        this.ip = getDokcerIp();

        this.redisPub = new Redis({ host: this.ip, port: 6379 });
        this.redisSub = new Redis({ host: this.ip, port: 6379 });
        
        for (let i=0;i<=7;i++){
            this.doors.push({
                localidade: i,
                status: 'fechada',
            });
        }

        this.redis.subscribe('elevator-state', (state) =>{
            this.handleElevatorState(state);
        })
    };

    async handleElevatorState(state: any){
        const { floor, status } = state;

        console.log('Elevator state received:', state);

        if(status === 'parado'){
            await this.openCloseDoor(floor);
        }
    }

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


        this.redisSub.subscribe('doors:commands', (err)=> {
            if (err) console.error('Subscribe error:', err);
            else console.log('Backend-doors inscrito no canal elevator:commands');
        });

        this.redisSub.on('message', (channel, message) => {
            console.log(`Recebido do elevador no canal ${channel}:`, message);
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
            JSON.stringify({
                type: 'call',
                floor,
                source: 'door',
            })
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
