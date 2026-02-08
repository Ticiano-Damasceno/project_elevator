from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.lifespan import lifespan
from .infra.api.routes.elevator_routes import router

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:4000','http://127.0.0.1:4000'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(
    router,
    prefix="/elevator",
    tags=["Elevator"]
)

@app.get("/ping")
def health():
    return {"status": "ok"}