from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    VectorSearch,
    VectorSearchProfile,
)

from app.core.config import get_settings


class AzureSearchIndexService:
    def __init__(self) -> None:
        settings = get_settings()

        self.client = SearchIndexClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            credential=AzureKeyCredential(
                settings.AZURE_SEARCH_API_KEY,
            ),
        )

    def create_index(self) -> SearchIndex:
        settings = get_settings()

        fields = [
            SearchField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
                filterable=True,
            ),
            SearchField(
                name="document_id",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            SearchField(
                name="chunk_index",
                type=SearchFieldDataType.Int32,
                filterable=True,
                sortable=True,
            ),
            SearchField(
                name="filename",
                type=SearchFieldDataType.String,
                searchable=True,
                filterable=True,
            ),
            SearchField(
                name="content",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(
                    SearchFieldDataType.Single,
                ),
                searchable=True,
                vector_search_dimensions=384,
                vector_search_profile_name="content-vector-profile",
            ),
        ]

        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="content-hnsw",
                ),
            ],
            profiles=[
                VectorSearchProfile(
                    name="content-vector-profile",
                    algorithm_configuration_name="content-hnsw",
                ),
            ],
        )

        index = SearchIndex(
            name=settings.AZURE_SEARCH_INDEX_NAME,
            fields=fields,
            vector_search=vector_search,
        )

        return self.client.create_or_update_index(index)