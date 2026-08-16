import os

os.environ["REDIS_URL"] = "redis://localhost:6379/0"

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker, engine


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def cleanup_database_engine():
    await engine.dispose()
    yield
    await engine.dispose()