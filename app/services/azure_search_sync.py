from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.azure_search import AzureSearchService


class AzureSearchSyncService:
    def __init__(self) -> None:
        self.search_service = AzureSearchService()

    def build_document(
        self,
        document: Document,
        chunk: DocumentChunk,
    ) -> dict[str, object]:
        return {
            "id": str(chunk.id),
            "document_id": str(document.id),
            "chunk_index": chunk.chunk_index,
            "filename": document.filename,
            "content": chunk.content,
            "embedding": chunk.embedding,
        }

    def upload_document(
        self,
        document: Document,
        chunk: DocumentChunk,
    ) -> None:
        search_document = self.build_document(
            document=document,
            chunk=chunk,
        )

        self.search_service.client.upload_documents(
            documents=[search_document],
        )

    def delete_documents(
        self,
        document_ids: list[str],
    ) -> None:
        self.search_service.client.delete_documents(
            documents=[
                {"id": document_id}
                for document_id in document_ids
            ],
        )    