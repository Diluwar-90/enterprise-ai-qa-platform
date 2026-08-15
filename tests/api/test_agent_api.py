from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.exceptions import AgentExecutionError
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
    body = response.json()
    assert body["answer"] == (
            "The Enterprise Knowledge Intelligence Platform "
            "is an AI-powered enterprise knowledge system."
        )

    assert body["request_id"]   
    assert response.headers["X-Request-ID"] == body["request_id"]

def test_agent_query_execution_error() -> None:
    with patch(
        "app.api.agent.AgentService.run",
        new=AsyncMock(
            side_effect=AgentExecutionError(
                "Agent execution failed.",
            ),
        ),
    ):
        client = TestClient(app)

        response = client.post(
            "/agent/query",
            json={
                "query": "What is the platform?",
            },
        )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "The agent service is temporarily unavailable."
    }

def test_agent_query_rejects_empty_query() -> None:
    client = TestClient(app)

    response = client.post(
        "/agent/query",
        json={
            "query": "",
        },
    )

    assert response.status_code == 422


def test_agent_query_rejects_query_over_2000_characters() -> None:
    client = TestClient(app)

    response = client.post(
        "/agent/query",
        json={
            "query": "a" * 2001,
        },
    )

    assert response.status_code == 422