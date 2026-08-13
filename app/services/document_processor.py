from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.services.azure_search_sync import AzureSearchSyncService
from app.services.chunking import DocumentChunker
from app.services.document_parser import DocumentParser
from app.services.embeddings.service import EmbeddingService


class DocumentProcessor:
    def __init__(self) -> None:
        self.parser = DocumentParser()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()
        self.azure_search_sync = AzureSearchSyncService()

    async def process(
        self,
        document: Document,
        db: AsyncSession,
    ) -> list[DocumentChunk]:
        document.status = DocumentStatus.PROCESSING

        text = await self.parser.parse(
            document.storage_path,
            document.content_type,
        )

        if not text.strip():
            document.status = DocumentStatus.FAILED
            document.error_message = "No text could be extracted."
            await db.commit()

            raise ValueError("No text could be extracted from document.")

        chunks = self.chunker.split(text)

        embeddings = self.embedding_service.embed_documents(chunks)

        document_chunks = [
            DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )
            for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings, strict=True)
            )
        ]

        db.add_all(document_chunks)

        document.status = DocumentStatus.PROCESSED
        document.error_message = None

        await db.commit()
        for chunk in document_chunks:
            self.azure_search_sync.upload_document(
                document=document,
                chunk=chunk,
            )

        return document_chunks