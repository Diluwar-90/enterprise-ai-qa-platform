from unittest.mock import AsyncMock, patch

import pytest

from app.agents.graph import build_agent_graph


@pytest.mark.asyncio
async def test_agent_graph_knowledge_route() -> None:
    graph = build_agent_graph()

    with (
        patch(
            "app.agents.nodes.RetrievalTool.search",
           new=AsyncMock(
                return_value=(
                    "[Chunk 0]\n"
                     "Enterprise Knowledge Intelligence Platform"
                ),
            ),
        ),
        patch(
            "app.agents.nodes.LLMService.generate",
            new=AsyncMock(
                return_value=(
                    "The platform is an enterprise knowledge system."
                ),
            ),
        ),
    ):
        result = await graph.ainvoke(
            {
                "query": (
                    "What is the Enterprise Knowledge "
                    "Intelligence Platform?"
                ),
            }
        )

    assert result["route"] == "knowledge"
    assert result["context"] == (
        "[Chunk 0]\nEnterprise Knowledge Intelligence Platform"
    )
    assert result["answer"] == (
        "The platform is an enterprise knowledge system."
    )


@pytest.mark.asyncio
async def test_agent_graph_direct_route() -> None:
    graph = build_agent_graph()

    with (
        patch(
            "app.agents.nodes.RetrievalTool.search",
            new=AsyncMock(),
        ) as mock_retrieve,
        patch(
            "app.agents.nodes.LLMService.generate",
            new=AsyncMock(
                return_value="Hello! How can I help you?",
            ),
        ) as mock_generate,
    ):
        result = await graph.ainvoke(
            {
                "query": "Hello",
            }
        )

    assert result["route"] == "direct"
    assert result["answer"] == "Hello! How can I help you?"

    mock_retrieve.assert_not_awaited()
    mock_generate.assert_awaited_once()

@pytest.mark.asyncio
async def test_agent_graph_sensitive_sql_requires_approval() -> None:
    graph = build_agent_graph()

    with patch(
        "app.agents.nodes.SQLAgentService.generate_query",
        new=AsyncMock(
            return_value="SELECT email FROM users",
        ),
    ):
        result = await graph.ainvoke(
            {
                "query": "Show me user emails",
            }
        )

    assert result["route"] == "sql"
    assert result["sql_query"] == "SELECT email FROM users"
    assert result["action"] == "sensitive_data_access"
    assert result["approval_required"] is True
    assert result["approval_status"] == "pending"
    assert result["answer"] == (
    "Human approval is required before accessing sensitive data."
)