from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.rag import RAGService


@pytest.mark.asyncio
async def test_rag_answer(
    db_session: AsyncSession,
) -> None:
    with patch("app.services.rag.LLMService") as mock_llm:
        mock_llm.return_value.generate = AsyncMock(
            return_value="The platform provides enterprise AI capabilities.",
        )

        rag_service = RAGService()

        with patch.object(
            rag_service.retrieval,
            "retrieve",
            new=AsyncMock(
                return_value=SimpleNamespace(
                    context="[Chunk 0]\nEnterprise AI platform documentation.",
                    chunks=[],
                ),
            ),
        ):
            result = await rag_service.answer(
                db=db_session,
                query="What does the platform provide?",
                limit=5,
            )

    assert result == "The platform provides enterprise AI capabilities."
    mock_llm.return_value.generate.assert_awaited_once()