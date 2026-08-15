from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.nodes import AgentNodes
from app.agents.state import AgentState


@pytest.mark.asyncio
async def test_retrieve_node() -> None:
    nodes = AgentNodes()

    retrieval_result = MagicMock()
    retrieval_result.context = (
        "[Chunk 0]\nEnterprise Knowledge Intelligence Platform"
    )

    with patch.object(
        nodes.retrieval,
        "retrieve_hybrid",
        new=AsyncMock(return_value=retrieval_result),
    ) as mock_retrieve:
        state = AgentState(
            query="What is the Enterprise Knowledge Intelligence Platform?"
        )

        result = await nodes.retrieve(state)

    mock_retrieve.assert_awaited_once_with(
        query="What is the Enterprise Knowledge Intelligence Platform?",
        limit=5,
    )

    assert result == {
        "context": "[Chunk 0]\nEnterprise Knowledge Intelligence Platform"
    }


@pytest.mark.asyncio
async def test_generate_node() -> None:
    nodes = AgentNodes()

    with patch.object(
        nodes.llm,
        "generate",
        new=AsyncMock(
            return_value="The platform is an enterprise knowledge system.",
        ),
    ) as mock_generate:
        state = AgentState(
            query="What is the Enterprise Knowledge Intelligence Platform?",
            context=(
                "[Chunk 0]\n"
                "The platform is an enterprise knowledge system."
            ),
        )

        result = await nodes.generate(state)

    mock_generate.assert_awaited_once()

    assert result == {
        "answer": "The platform is an enterprise knowledge system."
    }


@pytest.mark.asyncio
async def test_generate_node_without_context() -> None:
    nodes = AgentNodes()

    with patch.object(
        nodes.llm,
        "generate",
        new=AsyncMock(),
    ) as mock_generate:
        state = AgentState(
            query="What is the vacation policy?",
            route="knowledge",
            context="",
        )

        result = await nodes.generate(state)

    assert result == {
        "answer": "I do not have enough information to answer."
    }
    mock_generate.assert_not_awaited()


def test_route_knowledge_query() -> None:
    nodes = AgentNodes()

    state = AgentState(
        query="What is the Enterprise Knowledge Intelligence Platform?"
    )

    result = nodes.route(state)

    assert result == {"route": "knowledge"}


def test_route_direct_query() -> None:
    nodes = AgentNodes()

    state = AgentState(
        query="Hello"
    )

    result = nodes.route(state)

    assert result == {"route": "direct"}