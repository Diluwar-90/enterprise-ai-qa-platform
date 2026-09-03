from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.services.embeddings.service import EmbeddingService
from app.services.retrieval import RetrievalService
from unittest.mock import MagicMock, patch


@pytest.mark.asyncio
async def test_retrieval(
    db_session: AsyncSession,
) -> None:
    embedding_service = EmbeddingService()
    retrieval_service = RetrievalService()

    document = Document(
        owner_id="11111111-1111-1111-1111-111111111111",
        filename="retrieval-test.txt",
        content_type="text/plain",
        file_size=10,
        status=DocumentStatus.PROCESSED,
        storage_path="test/retrieval-test.txt",
    )

    db_session.add(document)
    await db_session.flush()

    content = "Enterprise Knowledge Intelligence Platform"

    chunk = DocumentChunk(
        document_id=document.id,
        chunk_index=0,
        content=content,
        embedding=embedding_service.embed_text(content),
    )

    db_session.add(chunk)
    await db_session.commit()

    results = await retrieval_service.retrieve(
        db=db_session,
        query="Enterprise Knowledge Intelligence Platform",
        limit=1,
    )

    assert "[Chunk 0]" in results.context
    assert len(results.chunks) == 1
    assert results.chunks[0].chunk_index == 0
    assert content in results.context

@pytest.mark.asyncio
async def test_retrieval_rejects_irrelevant_results(
    db_session: AsyncSession,
) -> None:
    embedding_service = EmbeddingService()
    retrieval_service = RetrievalService()

    document = Document(
        owner_id="11111111-1111-1111-1111-111111111111",
        filename="irrelevant-test.txt",
        content_type="text/plain",
        file_size=10,
        status=DocumentStatus.PROCESSED,
        storage_path="test/irrelevant-test.txt",
    )

    db_session.add(document)
    await db_session.flush()

    content = "This document contains unrelated information."

    chunk = DocumentChunk(
        document_id=document.id,
        chunk_index=0,
        content=content,
        embedding=embedding_service.embed_text(content),
    )

    db_session.add(chunk)
    await db_session.commit()

    results = await retrieval_service.retrieve(
        db=db_session,
        query="Completely unrelated question about quantum computing",
        limit=1,
    )

    assert results.chunks == []
    assert results.context == "" 

@pytest.mark.asyncio
async def test_retrieve_hybrid(
    db_session: AsyncSession,
) -> None:
    chunk_id = uuid4()
    document_id = uuid4()

    retrieval_service = RetrievalService()

    retrieval_service.azure_search.hybrid_search = MagicMock(
        return_value=[
            {
                "id": str(chunk_id),
                "document_id": str(document_id),
                "chunk_index": 0,
                "filename": "test_knowledge.txt",
                "content": "Enterprise Knowledge Intelligence Platform",
            }
        ]
    )

    with patch(
        "app.services.retrieval.get_settings"
    ) as mock_get_settings:
        mock_get_settings.return_value.RETRIEVAL_PROVIDER = "azure"

        result = await retrieval_service.retrieve_hybrid(
            query="What is the Enterprise Knowledge Intelligence Platform?",
            limit=5,
        )

    assert len(result.chunks) == 1
    assert result.chunks[0].id == chunk_id
    assert result.chunks[0].document_id == document_id
    assert result.chunks[0].chunk_index == 0
    assert result.chunks[0].content == (
        "Enterprise Knowledge Intelligence Platform"
    )                                                                                                                                                              