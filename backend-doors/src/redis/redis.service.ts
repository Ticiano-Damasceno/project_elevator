import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { createClient, RedisClientType } from 'redis';

@Injectable()
export class RedisService implements OnModuleInit,OnModuleDestroy{
    private client: RedisClientType;

    async onModuleInit(){
        const host = process.env.REDIS_HOST || 'localhost';
        const port = Number(process.env.REDIS_PORT) || 6379;

        this.client = createClient({ socket: { host,port } });

        this.client.on('error', err => console.error('Redis eror:', err));

        await this.client.connect();
        console.log(`Conectado ao redis em ${host}:${port}`);
    }

    async onModuleDestroy() {
        await this.client.quit();
    }

    getClient() {
        return this.client;
    }
};