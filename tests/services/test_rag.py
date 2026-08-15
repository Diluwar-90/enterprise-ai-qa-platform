from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import LLMGenerationError
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
                    chunks=[MagicMock()],
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
    assert len(retrieval_result.chunks) == 1
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
            chunks=[MagicMock()],
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

@pytest.mark.asyncio
async def test_rag_insufficient_information() -> None:
    with patch("app.services.rag.LLMService") as mock_llm:
        mock_llm.return_value.generate = AsyncMock(
            return_value="I do not have enough information to answer.",
        )

        rag_service = RAGService()

        retrieval_result = SimpleNamespace(
            context="[Chunk 0]\nThis document contains information about databases.",
            chunks=[],
        )

        with patch.object(
            rag_service.retrieval,
            "retrieve",
            new=AsyncMock(return_value=retrieval_result),
        ):
            answer, _ = await rag_service.answer(
                db=MagicMock(),
                query="What is the company's vacation policy?",
            )

        assert answer == "I do not have enough information to answer."     

@pytest.mark.asyncio
async def test_rag_returns_insufficient_information_when_no_chunks() -> None:
    rag_service = RAGService()

    retrieval_result = SimpleNamespace(
        context="",
        chunks=[],
    )

    with patch.object(
        rag_service.retrieval,
        "retrieve",
        new=AsyncMock(return_value=retrieval_result),
    ), patch.object(
        rag_service.llm,
        "generate",
        new=AsyncMock(),
    ) as mock_generate:
        answer, result = await rag_service.answer(
            db=MagicMock(),
            query="What is the vacation policy?",
        )

    assert answer == "I do not have enough information to answer."
    assert result is retrieval_result
    mock_generate.assert_not_awaited()


@pytest.mark.asyncio
async def test_hybrid_rag_returns_insufficient_information_when_no_chunks() -> None:
    rag_service = RAGService()

    retrieval_result = SimpleNamespace(
        context="",
        chunks=[],
    )

    with patch.object(
        rag_service.retrieval,
        "retrieve_hybrid",
        new=AsyncMock(return_value=retrieval_result),
    ), patch.object(
        rag_service.llm,
        "generate",
        new=AsyncMock(),
    ) as mock_generate:
        answer, result = await rag_service.answer_hybrid(
            query="What is the vacation policy?",
        )

    assert answer == "I do not have enough information to answer."
    assert result is retrieval_result
    mock_generate.assert_not_awaited()

@pytest.mark.asyncio
async def test_rag_propagates_llm_generation_error() -> None:
    rag_service = RAGService()

    retrieval_result = SimpleNamespace(
        context="[Chunk 0]\nEnterprise AI platform documentation.",
        chunks=[MagicMock()],
    )

    with (
        patch.object(
            rag_service.retrieval,
            "retrieve_hybrid",
            new=AsyncMock(return_value=retrieval_result),
        ),
        patch.object(
            rag_service.llm,
            "generate",
            new=AsyncMock(
                side_effect=LLMGenerationError("LLM unavailable"),
            ),
        ),pytest.raises(LLMGenerationError, match="LLM unavailable")
    ):
        await rag_service.answer_hybrid(
            query="What does the platform provide?",
        )   