from unittest.mock import AsyncMock, patch

import pytest

from app.agents.nodes import AgentNodes
from app.agents.state import AgentState


@pytest.mark.asyncio
async def test_retrieve_node() -> None:
    nodes = AgentNodes()

    retrieval_result = AsyncMock()
    retrieval_result = (
        "[Chunk 0]\nEnterprise Knowledge Intelligence Platform"
    )

    with patch.object(
        nodes.retrieval,
        "search",
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

@pytest.mark.asyncio
async def test_retrieve_node_handles_tool_failure() -> None:
    nodes = AgentNodes()

    with patch.object(
        nodes.retrieval,
        "search",
        new=AsyncMock(
            side_effect=RuntimeError("Retrieval tool failed."),
        ),
    ) as mock_retrieve:
        state = AgentState(
            query="What is the platform?"
        )

        result = await nodes.retrieve(state)

    mock_retrieve.assert_awaited_once_with(
        query="What is the platform?",
        limit=5,
    )

    assert result == {
        "context": "",
        "error": "Retrieval tool failed.",
    }

@pytest.mark.asyncio
async def test_generate_node_with_retrieval_error() -> None:
    nodes = AgentNodes()

    with patch.object(
        nodes.llm,
        "generate",
        new=AsyncMock(),
    ) as mock_generate:
        state = AgentState(
            query="What is the platform?",
            route="knowledge",
            error="Retrieval tool failed.",
        )

        result = await nodes.generate(state)

    assert result == {
        "answer": "Unable to retrieve knowledge at this time.",
    }

    mock_generate.assert_not_awaited()

def test_route_sql_query() -> None:
    nodes = AgentNodes()

    state = AgentState(
        query="How many documents are in the system?"
    )

    result = nodes.route(state)

    assert result == {"route": "sql"}


def test_route_sql_users_query() -> None:
    nodes = AgentNodes()

    state = AgentState(
        query="Show me the users"
    )

    result = nodes.route(state)

    assert result == {"route": "sql"}

@pytest.mark.asyncio
async def test_sql_execute_node() -> None:
    nodes = AgentNodes()

    with patch.object(
        nodes.sql,
        "execute",
        new=AsyncMock(
            return_value="{'count': 5}",
        ),
    ) as mock_execute:
        state = AgentState(
            query="How many documents are in the system?",
            route="sql",
            sql_query="SELECT COUNT(*) AS count FROM documents",
        )

        result = await nodes.sql_execute(state)

    mock_execute.assert_awaited_once_with(
        "SELECT COUNT(*) AS count FROM documents"
    )

    assert result == {
        "sql_result": "{'count': 5}",
    }

@pytest.mark.asyncio
async def test_generate_node_with_sql_result() -> None:
    nodes = AgentNodes()

    with patch.object(
        nodes.llm,
        "generate",
        new=AsyncMock(
            return_value="There are 5 documents in the system.",
        ),
    ) as mock_generate:
        state = AgentState(
            query="How many documents are in the system?",
            route="sql",
            sql_result="{'count': 5}",
        )

        result = await nodes.generate(state)

    mock_generate.assert_awaited_once()
    prompt = mock_generate.call_args.args[0]

    assert "There are 5 documents in the system." == result["answer"]
    assert "{'count': 5}" in prompt
    assert "How many documents are in the system?" in prompt

@pytest.mark.asyncio
async def test_classify_sql_action_node() -> None:
    nodes = AgentNodes()

    state = AgentState(
        query="Show me user emails",
        route="sql",
        sql_query="SELECT email FROM users",
    )

    result = await nodes.classify_sql_action(state)

    assert result == {
        "action": "sensitive_data_access",
    }

@pytest.mark.asyncio
async def test_classify_normal_sql_action_node() -> None:
    nodes = AgentNodes()

    state = AgentState(
        query="How many documents are in the system?",
        route="sql",
        sql_query="SELECT COUNT(*) FROM documents",
    )

    result = await nodes.classify_sql_action(state)

    assert result == {
        "action": "sql_read",
    }

def test_check_approval_for_sensitive_action() -> None:
    nodes = AgentNodes()

    state = AgentState(
        query="Show me user emails",
        route="sql",
        sql_query="SELECT email FROM users",
        action="sensitive_data_access",
    )

    result = nodes.check_approval(state)

    assert result == {
        "approval_required": True,
        "approval_status": "pending",
        "answer": (
            "Human approval is required before accessing sensitive data."
        ),
    }


def test_check_approval_for_normal_sql_read() -> None:
    nodes = AgentNodes()

    state = AgentState(
        query="How many documents are in the system?",
        route="sql",
        sql_query="SELECT COUNT(*) FROM documents",
        action="sql_read",
    )

    result = nodes.check_approval(state)

    assert result == {
        "approval_required": False,
        "approval_status": "not_required",
    }