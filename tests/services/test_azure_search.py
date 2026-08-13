from unittest.mock import MagicMock

from app.services.azure_search import AzureSearchService


def test_vector_search() -> None:
    service = AzureSearchService()
    service.client = MagicMock()

    service.client.search.return_value = [
        {
            "id": "chunk-1",
            "document_id": "document-1",
            "chunk_index": 0,
            "filename": "test_knowledge.txt",
            "content": "Enterprise Knowledge Intelligence Platform",
            "@search.score": 0.95,
        }
    ]

    query_embedding = [0.1, 0.2, 0.3]

    results = service.vector_search(
        query_embedding=query_embedding,
        limit=5,
    )

    assert len(results) == 1
    assert results[0]["filename"] == "test_knowledge.txt"
    assert results[0]["content"] == (
        "Enterprise Knowledge Intelligence Platform"
    )

    service.client.search.assert_called_once()

def test_hybrid_search() -> None:
    service = AzureSearchService()
    service.client = MagicMock()

    service.client.search.return_value = [
        {
            "id": "chunk-1",
            "document_id": "document-1",
            "chunk_index": 0,
            "filename": "test_knowledge.txt",
            "content": "Enterprise Knowledge Intelligence Platform",
            "@search.score": 1.25,
        }
    ]

    results = service.hybrid_search(
        query="What is the Enterprise Knowledge Intelligence Platform?",
        query_embedding=[0.1, 0.2, 0.3],
        limit=5,
    )

    assert len(results) == 1
    assert results[0]["filename"] == "test_knowledge.txt"
    assert results[0]["content"] == (
        "Enterprise Knowledge Intelligence Platform"
    )

    service.client.search.assert_called_once()    