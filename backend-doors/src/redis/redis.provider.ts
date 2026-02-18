import { Injectable } from '@nestjs/common';
import { Redis } from 'ioredis';

@Injectable()
export class RedisProvider{
    public pub: Redis;
    public sub: Redis;

    constructor(){
        const host = process.env.REDIS_HOST || 'localhost';
        const port = Number(process.env.REDIS_PORT) || 6379;

        this.pub = new Redis({ host, port});
        this.sub = new Redis({ host, port});
    }

    publish(channel: string, message: any){
        return this.pub.publish(channel, JSON.stringify(message));
    }

    subscribe(channel: string, handler: (msg: any) => void) {
        this.sub.subscribe(channel);
        this.sub.on('message', (_,message) =>{
            handler(JSON.stringify(message));
        });
    }
}