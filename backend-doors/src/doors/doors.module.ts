import { Module } from '@nestjs/common';
import { DoorsController } from './doors.controller';
import { DoorsService } from './doors.service';
import { RedisModule } from '../redis/redis.module';

@Module({
  imports: [RedisModule],
  controllers: [DoorsController],
  providers: [DoorsService]
})
export class DoorsModule {}
