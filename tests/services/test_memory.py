import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.memory import MemoryService


@pytest.mark.asyncio
async def test_add_and_get_short_term_memory() -> None:
    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock()

    with patch(
        "app.services.memory.RedisService",
        return_value=mock_redis,
    ):
        service = MemoryService()

        await service.add_short_term(
            session_id="session-1",
            query="What is the platform?",
            answer="It is an enterprise knowledge platform.",
        )

        mock_redis.get.assert_awaited_once_with(
            "memory:short:session-1"
        )

        mock_redis.set.assert_awaited_once_with(
            "memory:short:session-1",
            json.dumps(
                [
                    {
                        "query": "What is the platform?",
                        "answer": "It is an enterprise knowledge platform.",
                    }
                ]
            ),
            expire_seconds=3600,
        )


@pytest.mark.asyncio
async def test_get_short_term_memory() -> None:
    memories = [
        {
            "query": "What is the platform?",
            "answer": "Enterprise platform.",
        }
    ]

    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(
        return_value=json.dumps(memories)
    )
    mock_redis.set = AsyncMock()

    with patch(
        "app.services.memory.RedisService",
        return_value=mock_redis,
    ):
        service = MemoryService()

        result = await service.get_short_term("session-1")

    assert result == memories

    mock_redis.get.assert_awaited_once_with(
        "memory:short:session-1"
    )


@pytest.mark.asyncio
async def test_short_term_memory_keeps_last_ten_interactions() -> None:
    existing = [
        {
            "query": f"query-{index}",
            "answer": f"answer-{index}",
        }
        for index in range(10)
    ]

    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(
        return_value=json.dumps(existing)
    )
    mock_redis.set = AsyncMock()

    with patch(
        "app.services.memory.RedisService",
        return_value=mock_redis,
    ):
        service = MemoryService()

        await service.add_short_term(
            session_id="session-1",
            query="query-10",
            answer="answer-10",
        )

    saved = json.loads(
        mock_redis.set.await_args.args[1]
    )

    assert len(saved) == 10
    assert saved[0]["query"] == "query-1"
    assert saved[-1]["query"] == "query-10"


@pytest.mark.asyncio
async def test_add_and_get_long_term_memory() -> None:
    memory = {
        "type": "preference",
        "key": "response_style",
        "value": "concise",
    }

    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock()

    with patch(
        "app.services.memory.RedisService",
        return_value=mock_redis,
    ):
        service = MemoryService()

        await service.add_long_term(
            user_id="user-1",
            memory=memory,
        )

        mock_redis.set.assert_awaited_once_with(
            "memory:long:user-1",
            json.dumps([memory]),
        )


@pytest.mark.asyncio
async def test_get_long_term_memory() -> None:
    memories = [
        {
            "type": "preference",
            "key": "response_style",
            "value": "concise",
        }
    ]

    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(
        return_value=json.dumps(memories)
    )

    with patch(
        "app.services.memory.RedisService",
        return_value=mock_redis,
    ):
        service = MemoryService()

        result = await service.get_long_term("user-1")

    assert result == memories