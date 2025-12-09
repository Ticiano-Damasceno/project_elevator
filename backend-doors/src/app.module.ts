import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DoorsModule } from './doors/doors.module';

@Module({
  imports: [DoorsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
