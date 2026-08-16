from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.llm import LLMGenerationError, LLMService


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

def test_azure_provider() -> None:
    with patch(
        "app.services.llm.AsyncAzureOpenAI"
    ) as mock_client, patch(
        "app.services.llm.get_settings"
    ) as mock_settings:
        mock_settings.return_value.LLM_PROVIDER = "azure"
        mock_settings.return_value.AZURE_OPENAI_API_KEY = "test-key"
        mock_settings.return_value.AZURE_OPENAI_ENDPOINT = (
            "https://test.openai.azure.com/"
        )
        mock_settings.return_value.AZURE_OPENAI_API_VERSION = "2024-10-21"
        mock_settings.return_value.AZURE_OPENAI_DEPLOYMENT = (
            "enterprise-rag"
        )

        service = LLMService()

        mock_client.assert_called_once_with(
            api_key="test-key",
            azure_endpoint="https://test.openai.azure.com/",
            api_version="2024-10-21",
        )

        assert service.provider == "azure"
        assert service.model == "enterprise-rag"

@pytest.mark.asyncio
async def test_generate_raises_llm_generation_error() -> None:
    with (
         patch("app.services.llm.AsyncOpenAI") as mock_client,
         patch("app.services.llm.get_settings") as mock_settings
         ):
            mock_settings.return_value.LLM_PROVIDER = "openai"
            mock_settings.return_value.OPENAI_API_KEY = "test-key"
            mock_settings.return_value.OPENAI_MODEL = "gpt-4o-mini"

            mock_client.return_value.chat.completions.create = AsyncMock(
                side_effect=RuntimeError("provider unavailable"),
            )

            service = LLMService()

            with pytest.raises(LLMGenerationError, match="LLM generation failed"):
                await service.generate("test prompt")    

@pytest.mark.asyncio
async def test_generate_raises_error_for_empty_response() -> None:
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="",
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

        with pytest.raises(
            LLMGenerationError,
            match="LLM returned an empty response",
        ):
            await service.generate("Test prompt")    