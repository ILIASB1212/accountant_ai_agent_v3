from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from src.backend.config import Config

# libpq-only params that asyncpg does not accept
LIBPQ_ONLY_KEYS = {"sslmode", "channel_binding", "options"}

def clean_asyncpg_url(url: str) -> str:
    """Strip libpq-only query params so asyncpg won't choke on them."""
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query)
             if k not in LIBPQ_ONLY_KEYS]
    return urlunsplit(parts._replace(query=urlencode(query)))

engine = create_async_engine(
    clean_asyncpg_url(Config.DATABASE_URL),
    echo=True,
    connect_args={"ssl": "require"},   # asyncpg-style SSL
)


async def init_db():
    async with engine.begin() as conn:
        result = await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        if result.returns_rows:
            print(result.all())