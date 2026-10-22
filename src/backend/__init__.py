from fastapi import FastAPI
from src.backend.agent.endpoint import agent_router
from src.backend.auth.main import auth_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Starting up...")
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
app.include_router(auth_router, prefix=f"/api/{version}/registration", tags=['registration'])


