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