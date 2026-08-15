from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.tools.retrieval import RetrievalTool


@pytest.mark.asyncio
async def test_retrieval_tool_search() -> None:
    tool = RetrievalTool()

    retrieval_result = MagicMock()
    retrieval_result.context = (
        "[Chunk 0]\nEnterprise Knowledge Intelligence Platform"
    )

    with patch.object(
        tool.retrieval,
        "retrieve_hybrid",
        new=AsyncMock(return_value=retrieval_result),
    ) as mock_retrieve:
        result = await tool.search(
            query="What is the Enterprise Knowledge Intelligence Platform?",
            limit=5,
        )

    mock_retrieve.assert_awaited_once_with(
        query="What is the Enterprise Knowledge Intelligence Platform?",
        limit=5,
    )

    assert result == (
        "[Chunk 0]\nEnterprise Knowledge Intelligence Platform"
    )

@pytest.mark.asyncio
async def test_retrieval_tool_search_raises_runtime_error() -> None:
    tool = RetrievalTool()

    with patch.object(
        tool.retrieval,
        "retrieve_hybrid",
        new=AsyncMock(
            side_effect=Exception("Azure Search unavailable"),
        ),
    ), pytest.raises(
        RuntimeError,
        match="Retrieval tool failed.",
    ):
        await tool.search(
            query="What is the platform?",
            limit=5,
        )

def test_retrieval_tool_metadata() -> None:
    tool = RetrievalTool()

    assert tool.name == "knowledge_search"
    assert tool.description == (
        "Search enterprise knowledge and retrieve relevant document context."
    )