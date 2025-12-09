import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { createClient } from 'redis';

@Injectable()
export class RedisService implements OnModuleInit,OnModuleDestroy{
    private client;

    async onModuleInit(){
        this.client = createClient({
            url: process.env.REDIS_URL || 'redis://:6379',
        });

        this.client.on('error', err => console.error('Redis eror:', err));
    }

    async onModuleDestroy() {
        await this.client.quit();
    }

    getClient() {
        return this.client;
    }
}