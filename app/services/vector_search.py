
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.document_chunk import DocumentChunk


class VectorSearchService:
    async def search(
    self,
    db: AsyncSession,
    query_embedding: list[float],
    limit: int = 5,
) -> list[DocumentChunk]:
        statement = (
            select(DocumentChunk)
            .options(selectinload(DocumentChunk.document))
            .where(DocumentChunk.embedding != None)
            .order_by(
                DocumentChunk.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
        )

        result = await db.execute(statement)
        return result.scalars().all()