import os
from uuid import UUID

os.environ["REDIS_URL"] = "redis://localhost:6379/0"

import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker, engine
from app.models.user import User


TEST_USER_ID = UUID("11111111-1111-1111-1111-111111111111")


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.id == TEST_USER_ID)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                id=TEST_USER_ID,
                email="ci-test@example.com",
                full_name="CI Test User",
                is_active=True,
            )
            session.add(user)
            await session.flush()

        yield session


@pytest_asyncio.fixture(autouse=True)
async def cleanup_database_engine():
    await engine.dispose()
    yield
    await engine.dispose()