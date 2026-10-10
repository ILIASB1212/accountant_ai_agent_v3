from fastapi import FastAPI
from src.backend.agent.endpoint import agent_router
from contextlib import asynccontextmanager
from src.backend.db.main import init_db, engine

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Starting up...")
    await init_db()
    yield 
    print("Shutting down...")


version = "v3"

app = FastAPI(
            title="accounattant-agent",
            description="A REST API for the accountant-agent project",
            version= version,
            lifespan=life_span
)

app.include_router(agent_router, prefix=f"/api/{version}/agents", tags=['agent'])

