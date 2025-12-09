import { Test, TestingModule } from '@nestjs/testing';
import { DoorsController } from './doors.controller';

describe('DoorsController', () => {
  let controller: DoorsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [DoorsController],
    }).compile();

    controller = module.get<DoorsController>(DoorsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
