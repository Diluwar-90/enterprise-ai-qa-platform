from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.services.chunking import DocumentChunker
from app.services.document_parser import DocumentParser


class DocumentProcessor:
    def __init__(self) -> None:
        self.parser = DocumentParser()
        self.chunker = DocumentChunker()

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

        document_chunks = [
            DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
            )
            for index, chunk in enumerate(chunks)
        ]

        db.add_all(document_chunks)

        document.status = DocumentStatus.PROCESSED
        document.error_message = None

        await db.commit()

        return document_chunks