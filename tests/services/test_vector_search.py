import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.services.embeddings.service import EmbeddingService
from app.services.vector_search import VectorSearchService


@pytest.mark.asyncio
async def test_vector_search(
    db_session: AsyncSession,
) -> None:
    embedding_service = EmbeddingService()
    search_service = VectorSearchService()

    document = Document(
    owner_id="11111111-1111-1111-1111-111111111111",
    filename="vector-search-test.txt",
    content_type="text/plain",
    file_size=10,
    status=DocumentStatus.PROCESSED,
    storage_path="test/vector-search-test.txt",
)

    db_session.add(document)
    await db_session.flush()

    embedding = embedding_service.embed_text(
        "Enterprise Knowledge Intelligence Platform"
    )

    chunk = DocumentChunk(
        document_id=document.id,
        chunk_index=0,
        content="Enterprise Knowledge Intelligence Platform",
        embedding=embedding,
    )

    db_session.add(chunk)
    await db_session.commit()

    results = await search_service.search(
        db=db_session,
        query_embedding=embedding,
        limit=1,
    )

    assert len(results) == 1

    result_chunk, distance = results[0]

    assert result_chunk.content == "Enterprise Knowledge Intelligence Platform"
    assert distance == pytest.approx(0.0, abs=0.001)