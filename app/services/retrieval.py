from sqlalchemy.ext.asyncio import AsyncSession

from app.services.embeddings.service import EmbeddingService
from app.services.vector_search import VectorSearchService


class RetrievalService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_search = VectorSearchService()

    async def retrieve(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ):
        query_embedding = self.embedding_service.embed_text(query)

        return await self.vector_search.search(
            db=db,
            query_embedding=query_embedding,
            limit=limit,
        )