from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from app.core.config import get_settings


class AzureSearchService:
    def __init__(self) -> None:
        
        settings = get_settings()

        self.client = SearchClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            index_name=settings.AZURE_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(
                settings.AZURE_SEARCH_API_KEY,
            ),
        )

    def vector_search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[dict]:
        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=limit,
            fields="embedding",
        )

        results = self.client.search(
            search_text=None,
            vector_queries=[vector_query],
            top=limit,
        )

        return list(results)    

    def hybrid_search(
        self,
        query: str,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[dict]:
        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=limit,
            fields="embedding",
        )

        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            top=limit,
        )

        return list(results)