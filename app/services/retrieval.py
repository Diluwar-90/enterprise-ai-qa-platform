from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_chunk import DocumentChunk
from app.services.context_builder import ContextBuilder
from app.services.embeddings.service import EmbeddingService
from app.services.vector_search import VectorSearchService


@dataclass
class RetrievalResult:
    context: str
    chunks: list[DocumentChunk]


class RetrievalService:
    RELEVANCE_THRESHOLD = 0.6
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_search = VectorSearchService()
        self.context_builder = ContextBuilder()

    async def retrieve(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ) -> RetrievalResult:
        query_embedding = self.embedding_service.embed_text(query)

        search_results = await self.vector_search.search(
            db=db,
            query_embedding=query_embedding,
            limit=limit,
        )

        relevant_results = [
            (chunk, distance)
            for chunk, distance in search_results
            if distance <= self.RELEVANCE_THRESHOLD
        ]

        chunks = [chunk for chunk, _distance in relevant_results]

        context = self.context_builder.build(chunks)

        return RetrievalResult(
            context=context,
            chunks=chunks,
        )