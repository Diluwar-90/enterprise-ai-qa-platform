import pytest

from app.services.redis import RedisService


@pytest.mark.asyncio
async def test_redis_real_connection() -> None:
    service = RedisService()

    key = "test:redis:integration"
    value = "hello-redis"

    await service.set(
        key,
        value,
        expire_seconds=60,
    )

    result = await service.get(key)

    assert result == value

    await service.delete(key)

    result = await service.get(key)

    assert result is None

    await service.close()