from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.llm import LLMService


@pytest.mark.asyncio
async def test_llm_generate() -> None:
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="Test response",
            )
        )
    ]

    with patch(
        "app.services.llm.AsyncOpenAI",
    ) as mock_client:
        mock_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response,
        )

        service = LLMService()

        result = await service.generate("Test prompt")

        assert result == "Test response"