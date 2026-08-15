from fastapi.testclient import TestClient

from app.main import app
from app.services.llm import LLMGenerationError


def test_llm_generation_error_handler() -> None:
    @app.get("/test-llm-error")
    async def test_llm_error() -> None:
        raise LLMGenerationError("LLM unavailable")

    client = TestClient(app)

    response = client.get("/test-llm-error")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "The language model service is temporarily unavailable."
    }