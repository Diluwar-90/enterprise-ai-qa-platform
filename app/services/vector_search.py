
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
) -> list[tuple[DocumentChunk,float]]:
        statement = (
            select(DocumentChunk,DocumentChunk.embedding.cosine_distance(query_embedding),)
            .options(selectinload(DocumentChunk.document))
            .where(DocumentChunk.embedding != None)
            .order_by(
                DocumentChunk.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
        )

        result = await db.execute(statement)
        return [
            (chunk, float(distance))
            for chunk, distance in result.all()
        ]