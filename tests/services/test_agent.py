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

    with patch(
        "app.services.agent.build_agent_graph",
        return_value=mock_graph,
    ):
        service = AgentService()

        result = await service.run(
            "What is the platform?",
        )

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