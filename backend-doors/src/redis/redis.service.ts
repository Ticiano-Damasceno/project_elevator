import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { createClient } from 'redis';
import { getDokcerIp } from '../utils/getDockerIp';

@Injectable()
export class RedisService implements OnModuleInit,OnModuleDestroy{
    private client: any;

    async onModuleInit(){
        const ip = getDokcerIp();
        const redisUrl = `redis://${ip}:6379`
        this.client = createClient({
            url: process.env.REDIS_URL || redisUrl,
        });

        this.client.on('error', err => console.error('Redis eror:', err));

        await this.client.connect();
        console.log('Conectado ao redis com sucesso no endereço:', redisUrl);
    }

    async onModuleDestroy() {
        await this.client.quit();
    }

    getClient() {
        return this.client;
    }
}