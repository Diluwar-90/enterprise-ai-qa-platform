from app.services.azure_search import AzureSearchService
from app.services.embeddings.service import EmbeddingService


def main() -> None:
    embedding_service = EmbeddingService()
    search_service = AzureSearchService()

    query = "What is the Enterprise Knowledge Intelligence Platform?"

    query_embedding = embedding_service.embed_text(query)

    results = search_service.hybrid_search(
        query=query,
        query_embedding=query_embedding,
        limit=5,
    )

    for result in results:
        print(
            f"score={result.get('@search.score')} | "
            f"filename={result.get('filename')} | "
            f"chunk_index={result.get('chunk_index')}"
        )


if __name__ == "__main__":
    main()