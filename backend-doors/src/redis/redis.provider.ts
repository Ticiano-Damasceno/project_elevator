import { Injectable } from '@nestjs/common';
import { Redis } from 'ioredis';
import { getDokcerIp } from '../utils/getDockerIp';

@Injectable()
export class RedisProvider{
    public client: Redis;
    private ip: string;

    public pub: Redis;
    public sub: Redis;

    constructor(){
        this.ip = getDokcerIp();
        this.pub = new Redis({
            host: process.env.REDIS_HOST || this.ip,
            port: 6379,
        });
        this.sub = new Redis({
            host: process.env.REDIS_HOST || this.ip,
            port: 6379,
        });
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