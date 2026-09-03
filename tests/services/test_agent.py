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

    mock_conversation_memory = MagicMock()
    mock_conversation_memory.get_messages = AsyncMock(
        return_value=[]
    )
    mock_conversation_memory.add_message = AsyncMock()

    with (
        patch(
            "app.services.agent.build_agent_graph",
            return_value=mock_graph,
        ),
        patch(
            "app.services.agent.RedisService",
            return_value=mock_redis,
        ),
        patch(
            "app.services.agent.ConversationMemoryService",
            return_value=mock_conversation_memory,
        ),
    ):
        service = AgentService()

        result = await service.run(
            query="What is the platform?",
            session_id="session-1",
        )

    mock_conversation_memory.get_messages.assert_awaited_once_with(
        "session-1"
    )

    assert mock_conversation_memory.add_message.await_count == 2

    mock_redis.get.assert_awaited_once()

    mock_graph.ainvoke.assert_awaited_once_with(
        {
            "query": "What is the platform?",
            "conversation": [],
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

    mock_conversation_memory = MagicMock()
    mock_conversation_memory.get_messages = AsyncMock(
        return_value=[]
    )
    mock_conversation_memory.add_message = AsyncMock()

    with (
        patch(
            "app.services.agent.build_agent_graph",
            return_value=mock_graph,
        ),
        patch(
            "app.services.agent.RedisService",
            return_value=mock_redis,
        ),
        patch(
            "app.services.agent.ConversationMemoryService",
            return_value=mock_conversation_memory,
        ),
    ):
        service = AgentService()

        result = await service.run(
            query="How many documents are in the system?",
            session_id="session-1",
        )

    assert result == cached_response

    mock_conversation_memory.get_messages.assert_awaited_once_with(
        "session-1"
    )

    mock_conversation_memory.add_message.assert_not_awaited()

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

    mock_conversation_memory = MagicMock()
    mock_conversation_memory.get_messages = AsyncMock(
        return_value=[]
    )
    mock_conversation_memory.add_message = AsyncMock()

    with (
        patch(
            "app.services.agent.build_agent_graph",
            return_value=mock_graph,
        ),
        patch(
            "app.services.agent.RedisService",
            return_value=mock_redis,
        ),
        patch(
            "app.services.agent.ConversationMemoryService",
            return_value=mock_conversation_memory,
        ),
    ):
        service = AgentService()

        result = await service.run(
            query="How many documents are in the system?",
            session_id="session-1",
        )

    assert result == {
        "answer": "There are 5 documents.",
        "approval_required": False,
        "approval_status": "not_required",
        "action": "sql_read",
    }

    mock_conversation_memory.get_messages.assert_awaited_once_with(
        "session-1"
    )

    assert mock_conversation_memory.add_message.await_count == 2

    mock_redis.get.assert_awaited_once()

    mock_graph.ainvoke.assert_awaited_once_with(
        {
            "query": "How many documents are in the system?",
            "conversation": [],
        }
    )

    mock_redis.set.assert_awaited_once()


@pytest.mark.asyncio
async def test_agent_service_continues_when_redis_get_fails() -> None:
    mock_graph = MagicMock()

    mock_graph.ainvoke = AsyncMock(
        return_value={
            "query": "What is the platform?",
            "answer": "It is an enterprise knowledge platform.",
            "approval_required": False,
            "approval_status": "not_required",
            "action": None,
        },
    )

    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(
        side_effect=ConnectionError("Redis unavailable"),
    )
    mock_redis.set = AsyncMock()

    mock_conversation_memory = MagicMock()
    mock_conversation_memory.get_messages = AsyncMock(
        return_value=[]
    )
    mock_conversation_memory.add_message = AsyncMock()

    with (
        patch(
            "app.services.agent.build_agent_graph",
            return_value=mock_graph,
        ),
        patch(
            "app.services.agent.RedisService",
            return_value=mock_redis,
        ),
        patch(
            "app.services.agent.ConversationMemoryService",
            return_value=mock_conversation_memory,
        ),
    ):
        service = AgentService()

        result = await service.run(
            query="What is the platform?",
            session_id="session-1",
        )

    assert result == {
        "answer": "It is an enterprise knowledge platform.",
        "approval_required": False,
        "approval_status": "not_required",
        "action": None,
    }

    mock_conversation_memory.get_messages.assert_awaited_once_with(
        "session-1"
    )

    assert mock_conversation_memory.add_message.await_count == 2

    mock_redis.get.assert_awaited_once()

    mock_graph.ainvoke.assert_awaited_once_with(
        {
            "query": "What is the platform?",
            "conversation": [],
        }
    )


@pytest.mark.asyncio
async def test_agent_service_continues_when_redis_set_fails() -> None:
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
    mock_redis.set = AsyncMock(
        side_effect=ConnectionError("Redis unavailable"),
    )

    mock_conversation_memory = MagicMock()
    mock_conversation_memory.get_messages = AsyncMock(
        return_value=[]
    )
    mock_conversation_memory.add_message = AsyncMock()

    with (
        patch(
            "app.services.agent.build_agent_graph",
            return_value=mock_graph,
        ),
        patch(
            "app.services.agent.RedisService",
            return_value=mock_redis,
        ),
        patch(
            "app.services.agent.ConversationMemoryService",
            return_value=mock_conversation_memory,
        ),
    ):
        service = AgentService()

        result = await service.run(
            query="How many documents are in the system?",
            session_id="session-1",
        )

    assert result == {
        "answer": "There are 5 documents.",
        "approval_required": False,
        "approval_status": "not_required",
        "action": "sql_read",
    }

    mock_conversation_memory.get_messages.assert_awaited_once_with(
        "session-1"
    )

    assert mock_conversation_memory.add_message.await_count == 2

    mock_redis.get.assert_awaited_once()
    mock_redis.set.assert_awaited_once()

    mock_graph.ainvoke.assert_awaited_once_with(
        {
            "query": "How many documents are in the system?",
            "conversation": [],
        }
    )