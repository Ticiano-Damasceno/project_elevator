import { Module } from '@nestjs/common';
import { DoorsController } from './doors.controller';
import { DoorsService } from './doors.service';
import { RedisModule } from '../redis/redis.module';
import { RedisProvider } from '../redis/redis.provider';

@Module({
  imports: [RedisModule],
  controllers: [DoorsController],
  providers: [DoorsService, RedisProvider],
})
export class DoorsModule {}
