from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_first_request_is_allowed() -> None:
    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock()

    with patch(
        "app.services.rate_limiter.RedisService",
        return_value=mock_redis,
    ):
        limiter = RateLimiter()

        result = await limiter.is_allowed("client-1")

    assert result is True

    mock_redis.get.assert_awaited_once_with(
        "rate_limit:client-1",
    )

    mock_redis.set.assert_awaited_once_with(
        "rate_limit:client-1",
        "1",
        expire_seconds=limiter.window_seconds,
    )


@pytest.mark.asyncio
async def test_request_below_limit_is_allowed() -> None:
    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(return_value="2")
    mock_redis.set = AsyncMock()

    with patch(
        "app.services.rate_limiter.RedisService",
        return_value=mock_redis,
    ):
        limiter = RateLimiter()

        result = await limiter.is_allowed("client-1")

    assert result is True

    mock_redis.set.assert_awaited_once_with(
        "rate_limit:client-1",
        "3",
        expire_seconds=limiter.window_seconds,
    )


@pytest.mark.asyncio
async def test_request_at_limit_is_rejected() -> None:
    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(return_value="30")
    mock_redis.set = AsyncMock()

    with patch(
        "app.services.rate_limiter.RedisService",
        return_value=mock_redis,
    ):
        limiter = RateLimiter()

        result = await limiter.is_allowed("client-1")

    assert result is False
    mock_redis.set.assert_not_awaited()