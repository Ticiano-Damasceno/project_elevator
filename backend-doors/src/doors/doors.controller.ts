import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { DoorsService } from './doors.service';
import { openCloseDoorDto } from './dto/openCloseDoor.dto';

@Controller('doors')
export class DoorsController {
    constructor(private readonly doorsService: DoorsService){}

    @Get()
    getAllDoors(){
        return this.doorsService.getAllDoors();
    }

    @Get(':floor')
    getDoor(@Param('floor') floor: string){
        return this.doorsService.getDoorState(Number(floor));
    }

    @Post('open/:floor')
    async openDoor(@Param('floor') floor: string){
        console.log(`Iniciando a abertura manual da porta ${floor}.`)
        await this.doorsService.openDoor(Number(floor));
        return {}
    }

    @Post('close/:floor')
    async closeDoor(@Param('floor') floor: string){
        console.log(`Iniciando o fechamento manual da porta ${floor}.`)
        await this.doorsService.closeDoor(Number(floor));
        return { ok: true, "message": `Solicitado o fechamento manual da porta ${floor}` };
    }

    @Post('openCloseDoor/:floor')
    async openCloseDoor(@Param('floor') floor: string){
        await this.doorsService.openCloseDoor(Number(floor));
        return { ok: true, "message": `Solicitado abertura e fechamento manual da porta ${floor}` };
    }

    @Post('openClose')
    async openClose(@Body() dto: openCloseDoorDto){
        return this.doorsService.openCloseDoor(dto.doorId);
    }

    @Post('button/:floor')
    pressButton(@Param('floor') floor: string){
        return this.doorsService.pressButton(Number(floor));
    }

}
