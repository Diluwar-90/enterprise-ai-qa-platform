from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.redis import RedisService


@pytest.mark.asyncio
async def test_redis_set() -> None:
    mock_client = MagicMock()
    mock_client.set = AsyncMock()

    with patch(
        "app.services.redis.Redis.from_url",
        return_value=mock_client,
    ):
        service = RedisService()

        await service.set(
            "test:key",
            "test-value",
            expire_seconds=60,
        )

    mock_client.set.assert_awaited_once_with(
        "test:key",
        "test-value",
        ex=60,
    )


@pytest.mark.asyncio
async def test_redis_get() -> None:
    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value="test-value")

    with patch(
        "app.services.redis.Redis.from_url",
        return_value=mock_client,
    ):
        service = RedisService()

        result = await service.get("test:key")

    assert result == "test-value"


@pytest.mark.asyncio
async def test_redis_delete() -> None:
    mock_client = MagicMock()
    mock_client.delete = AsyncMock()

    with patch(
        "app.services.redis.Redis.from_url",
        return_value=mock_client,
    ):
        service = RedisService()

        await service.delete("test:key")

    mock_client.delete.assert_awaited_once_with("test:key")