from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


def test_agent_query() -> None:
    with patch(
        "app.api.agent.AgentService.run",
        new=AsyncMock(
            return_value=(
                "The Enterprise Knowledge Intelligence Platform "
                "is an AI-powered enterprise knowledge system."
            ),
        ),
    ):
        client = TestClient(app)

        response = client.post(
            "/agent/query",
            json={
                "query": "What is the Enterprise Knowledge Intelligence Platform?"
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "answer": (
            "The Enterprise Knowledge Intelligence Platform "
            "is an AI-powered enterprise knowledge system."
        )
    }