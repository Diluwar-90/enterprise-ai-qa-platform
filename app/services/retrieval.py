from sqlalchemy.ext.asyncio import AsyncSession

from app.services.context_builder import ContextBuilder
from app.services.embeddings.service import EmbeddingService
from app.services.vector_search import VectorSearchService


class RetrievalService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_search = VectorSearchService()
        self.context_builder = ContextBuilder()

    async def retrieve(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ) -> str:
        query_embedding = self.embedding_service.embed_text(query)

        chunks = await self.vector_search.search(
            db=db,
            query_embedding=query_embedding,
            limit=limit,
        )

        return self.context_builder.build(chunks)