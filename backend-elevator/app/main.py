from fastapi import FastAPI
from .core.lifespan import lifespan
from .infra.api.routes.elevator_routes import router

app = FastAPI(lifespan=lifespan)

app.include_router(router)