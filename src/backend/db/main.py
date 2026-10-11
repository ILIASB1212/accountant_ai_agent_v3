from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from src.backend.config import Config

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from sqlmodel import SQLModel



# libpq-only params that asyncpg does not accept
LIBPQ_ONLY_KEYS = {"sslmode", "channel_binding", "options"}

def clean_asyncpg_url(url: str) -> str:
    """Strip libpq-only query params so asyncpg won't choke on them."""
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query) if k not in LIBPQ_ONLY_KEYS]
    return urlunsplit(parts._replace(query=urlencode(query)))

async_engine = create_async_engine(
    clean_asyncpg_url(Config.DATABASE_URL),
    echo=True,
    connect_args={"ssl": "require"},   # asyncpg-style SSL
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)





async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session