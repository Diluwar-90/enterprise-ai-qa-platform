from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Enterprise Knowledge Intelligence Platform"
    assert data["version"] == "1.0.0"

def test_health_request_id_is_preserved() -> None:
    client = TestClient(app)

    response = client.get(
        "/health",
        headers={
            "X-Request-ID": "test-request-123",
        },
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-123"


def test_health_generates_request_id() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200

    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None
    assert len(request_id) > 0
