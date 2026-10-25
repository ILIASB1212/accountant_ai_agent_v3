import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from src.agentic_workflow.agent import build_graph
from src.backend.agent.endpoint import agent_router
from src.backend.auth.main import auth_router
from src.backend.config import Config

logger = logging.getLogger(__name__)

# The checkpointer creates its tables in `public`, which the Supabase Data API exposes.
# Turn RLS on (with no policies) so only this backend's direct connection can read them.
LOCK_CHECKPOINT_TABLES = """
do $$
declare t text;
begin
  for t in select tablename from pg_tables
           where schemaname = 'public' and tablename like 'checkpoint%'
  loop
    execute format('alter table public.%I enable row level security', t);
  end loop;
end $$;
"""


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting up...")
    pool = ConnectionPool(
        conninfo=Config.DATABASE_URL,
        max_size=10,
        # required by PostgresSaver; prepare_threshold=0 keeps Supabase's pooler happy
        kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},
        open=True,
    )
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()  # idempotent: creates the checkpoint tables on first run
    with pool.connection() as conn:
        conn.execute(LOCK_CHECKPOINT_TABLES)
    app.state.graph = build_graph(checkpointer)
    yield
    pool.close()
    print("Shutting down...")


version = "v3"

app = FastAPI(
    title="accounattant-agent",
    description="A REST API for the accountant-agent project",
    version=version,
    lifespan=life_span,
)

app.include_router(agent_router, prefix=f"/api/{version}/agents", tags=['agent'])
app.include_router(auth_router, prefix=f"/api/{version}/registration", tags=['registration'])
