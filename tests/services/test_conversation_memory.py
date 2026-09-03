from unittest.mock import AsyncMock

import pytest

from app.services.conversation_memory import ConversationMemoryService


@pytest.mark.asyncio
async def test_get_messages_returns_empty_when_memory_does_not_exist() -> None:
    service = ConversationMemoryService()
    service.redis.get = AsyncMock(return_value=None)

    result = await service.get_messages("session-1")

    assert result == []


@pytest.mark.asyncio
async def test_add_message() -> None:
    service = ConversationMemoryService()

    service.redis.get = AsyncMock(return_value=None)
    service.redis.set = AsyncMock()

    await service.add_message(
        session_id="session-1",
        role="user",
        content="What is RAG?",
    )

    service.redis.set.assert_awaited_once()

    args = service.redis.set.await_args.args
    kwargs = service.redis.set.await_args.kwargs

    assert args[0] == "conversation:memory:session-1"
    assert kwargs["expire_seconds"] == 3600


@pytest.mark.asyncio
async def test_get_messages() -> None:
    service = ConversationMemoryService()

    service.redis.get = AsyncMock(
        return_value='[{"role": "user", "content": "Hello"}]'
    )

    result = await service.get_messages("session-1")

    assert result == [
        {
            "role": "user",
            "content": "Hello",
        }
    ]


@pytest.mark.asyncio
async def test_clear() -> None:
    service = ConversationMemoryService()
    service.redis.delete = AsyncMock()

    await service.clear("session-1")

    service.redis.delete.assert_awaited_once_with(
        "conversation:memory:session-1"
    )