from types import SimpleNamespace
from unittest.mock import MagicMock
from uuid import uuid4

from app.services.azure_search_sync import AzureSearchSyncService


def test_build_document() -> None:
    document_id = uuid4()
    chunk_id = uuid4()

    document = SimpleNamespace(
        id=document_id,
        filename="test_knowledge.txt",
    )

    chunk = SimpleNamespace(
        id=chunk_id,
        document_id=document_id,
        chunk_index=0,
        content="Enterprise Knowledge Intelligence Platform",
        embedding=[0.1, 0.2, 0.3],
    )

    service = AzureSearchSyncService()

    result = service.build_document(
        document=document,
        chunk=chunk,
    )

    assert result == {
        "id": str(chunk_id),
        "document_id": str(document_id),
        "chunk_index": 0,
        "filename": "test_knowledge.txt",
        "content": "Enterprise Knowledge Intelligence Platform",
        "embedding": [0.1, 0.2, 0.3],
    }

def test_upload_document() -> None:
    document_id = uuid4()
    chunk_id = uuid4()

    document = SimpleNamespace(
        id=document_id,
        filename="test_knowledge.txt",
    )

    chunk = SimpleNamespace(
        id=chunk_id,
        document_id=document_id,
        chunk_index=0,
        content="Enterprise Knowledge Intelligence Platform",
        embedding=[0.1, 0.2, 0.3],
    )

    service = AzureSearchSyncService()
    service.search_service.client = MagicMock()

    service.upload_document(
        document=document,
        chunk=chunk,
    )

    service.search_service.client.upload_documents.assert_called_once_with(
        documents=[
            {
                "id": str(chunk_id),
                "document_id": str(document_id),
                "chunk_index": 0,
                "filename": "test_knowledge.txt",
                "content": "Enterprise Knowledge Intelligence Platform",
                "embedding": [0.1, 0.2, 0.3],
            }
        ]
    )  

def test_delete_documents() -> None:
    service = AzureSearchSyncService()
    service.search_service.client = MagicMock()

    document_ids = [
        "chunk-1",
        "chunk-2",
    ]

    service.delete_documents(document_ids)

    service.search_service.client.delete_documents.assert_called_once_with(
        documents=[
            {"id": "chunk-1"},
            {"id": "chunk-2"},
        ],
    )      