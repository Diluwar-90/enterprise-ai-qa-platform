import asyncio

from sqlalchemy import select

from app.db.session import async_session_maker
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.azure_search_sync import AzureSearchSyncService


async def sync_documents() -> None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Document, DocumentChunk)
            .join(
                DocumentChunk,
                DocumentChunk.document_id == Document.id,
            )
            .where(DocumentChunk.embedding.is_not(None))
        )

        rows = result.all()

        sync_service = AzureSearchSyncService()

        for document, chunk in rows:
            sync_service.upload_document(
                document=document,
                chunk=chunk,
            )

        print(f"Synced {len(rows)} chunks to Azure AI Search.")


if __name__ == "__main__":
    asyncio.run(sync_documents())