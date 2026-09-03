from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.azure_search import AzureSearchService
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
        self.azure_search = AzureSearchService()
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

    async def retrieve_hybrid(
        self,
        query: str,
        limit: int = 5,
    ) -> RetrievalResult:
        settings = get_settings()

        query_embedding = self.embedding_service.embed_text(query)

        if settings.RETRIEVAL_PROVIDER.lower() == "postgres":
            async with AsyncSessionLocal() as db:
                search_results = await self.vector_search.search(
                    db=db,
                    query_embedding=query_embedding,
                    limit=limit,
                )

            chunks = [
                chunk
                for chunk, _distance in search_results
            ]

        elif settings.RETRIEVAL_PROVIDER.lower() == "azure":
            results = self.azure_search.hybrid_search(
                query=query,
                query_embedding=query_embedding,
                limit=limit,
            )

            chunks = [
                DocumentChunk(
                    id=UUID(result["id"]),
                    document_id=UUID(result["document_id"]),
                    chunk_index=result["chunk_index"],
                    content=result["content"],
                    document=Document(
                        id=UUID(result["document_id"]),
                        filename=result["filename"],
                    ),
                )
                for result in results
            ]

        else:
            raise ValueError(
                f"Unsupported retrieval provider: "
                f"{settings.RETRIEVAL_PROVIDER}"
            )

        context = self.context_builder.build(chunks)

        return RetrievalResult(
            context=context,
            chunks=chunks,
        )