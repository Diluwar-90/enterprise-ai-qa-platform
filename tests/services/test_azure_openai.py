from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.azure_openai import AzureOpenAIService


@pytest.mark.asyncio
async def test_generate() -> None:
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="The platform provides enterprise AI capabilities.",
            )
        )
    ]

    with patch(
        "app.services.azure_openai.AsyncAzureOpenAI"
    ) as mock_client:
        mock_client.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response,
        )

        service = AzureOpenAIService()

        result = await service.generate(
            "What does the platform provide?"
        )

        assert result == (
            "The platform provides enterprise AI capabilities."
        )

        mock_client.return_value.chat.completions.create.assert_awaited_once()