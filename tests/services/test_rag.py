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
            answer, retrieval_result = await rag_service.answer(
                db=db_session,
                query="What does the platform provide?",
                limit=5,
            )

    assert answer == "The platform provides enterprise AI capabilities."
    assert retrieval_result.context == "[Chunk 0]\nEnterprise AI platform documentation."
    assert retrieval_result.chunks == []
    mock_llm.return_value.generate.assert_awaited_once()

@pytest.mark.asyncio
async def test_rag_hybrid_answer() -> None:
    with patch("app.services.rag.LLMService") as mock_llm:
        mock_llm.return_value.generate = AsyncMock(
            return_value="The platform provides enterprise AI capabilities.",
        )

        rag_service = RAGService()

        retrieval_result = SimpleNamespace(
            context="[Chunk 0]\nEnterprise AI platform documentation.",
            chunks=[],
        )

        with patch.object(
            rag_service.retrieval,
            "retrieve_hybrid",
            new=AsyncMock(return_value=retrieval_result),
        ):
            answer, result = await rag_service.answer_hybrid(
                query="What does the platform provide?",
                limit=5,
            )

        assert answer == "The platform provides enterprise AI capabilities."
        assert result is retrieval_result

        mock_llm.return_value.generate.assert_awaited_once()    