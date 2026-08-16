import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.agent import AgentService


@pytest.mark.asyncio
async def test_agent_service_run() -> None:
    mock_graph = MagicMock()

    mock_graph.ainvoke = AsyncMock(
        return_value={
            "query": "What is the platform?",
            "context": "Enterprise knowledge platform.",
            "answer": "It is an enterprise knowledge platform.",
        },
    )

    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock()

    with (
        patch(
            "app.services.agent.build_agent_graph",
            return_value=mock_graph,
        ),
        patch(
            "app.services.agent.RedisService",
            return_value=mock_redis,
        ),
    ):
        service = AgentService()

        result = await service.run(
            "What is the platform?",
        )

    mock_redis.get.assert_awaited_once()

    mock_graph.ainvoke.assert_awaited_once_with(
        {
            "query": "What is the platform?",
        }
    )

    assert result == {
        "answer": "It is an enterprise knowledge platform.",
        "approval_required": False,
        "approval_status": "not_required",
        "action": None,
    }

    mock_redis.set.assert_not_awaited()

@pytest.mark.asyncio
async def test_agent_service_returns_cached_response() -> None:
    mock_graph = MagicMock()
    mock_graph.ainvoke = AsyncMock()

    cached_response = {
        "answer": "There are 5 documents.",
        "approval_required": False,
        "approval_status": "not_required",
        "action": "sql_read",
    }

    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(
        return_value=json.dumps(cached_response),
    )
    mock_redis.set = AsyncMock()

    with (
        patch(
            "app.services.agent.build_agent_graph",
            return_value=mock_graph,
        ),
        patch(
            "app.services.agent.RedisService",
            return_value=mock_redis,
        ),
    ):
        service = AgentService()

        result = await service.run(
            "How many documents are in the system?",
        )

    assert result == cached_response

    mock_redis.get.assert_awaited_once()
    mock_redis.set.assert_not_awaited()
    mock_graph.ainvoke.assert_not_awaited()

@pytest.mark.asyncio
async def test_agent_service_caches_sql_read_response() -> None:
    mock_graph = MagicMock()

    mock_graph.ainvoke = AsyncMock(
        return_value={
            "query": "How many documents are in the system?",
            "answer": "There are 5 documents.",
            "approval_required": False,
            "approval_status": "not_required",
            "action": "sql_read",
        },
    )

    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock()

    with (
        patch(
            "app.services.agent.build_agent_graph",
            return_value=mock_graph,
        ),
        patch(
            "app.services.agent.RedisService",
            return_value=mock_redis,
        ),
    ):
        service = AgentService()

        result = await service.run(
            "How many documents are in the system?",
        )

    assert result == {
        "answer": "There are 5 documents.",
        "approval_required": False,
        "approval_status": "not_required",
        "action": "sql_read",
    }

    mock_redis.get.assert_awaited_once()

    mock_graph.ainvoke.assert_awaited_once_with(
        {
            "query": "How many documents are in the system?",
        }
    )

    mock_redis.set.assert_awaited_once()