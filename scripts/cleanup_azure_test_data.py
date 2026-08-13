import asyncio

from azure.search.documents import SearchClient
from sqlalchemy import select

from app.core.config import get_settings
from app.db.session import async_session_maker
from app.models.document import Document
from app.services.azure_search_sync import AzureSearchSyncService

TEST_FILENAMES = {
    "test.txt",
    "retrieval-test.txt",
    "vector-search-test.txt",
    "irrelevant-test.txt",
}


async def cleanup() -> None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Document.id, Document.filename)
            .where(Document.filename.in_(TEST_FILENAMES))
        )

        document_ids = [str(document_id) for document_id, _ in result.all()]

    if not document_ids:
        print("No test documents found.")
        return

    settings = get_settings()

    client = SearchClient(
        endpoint=settings.AZURE_SEARCH_ENDPOINT,
        index_name=settings.AZURE_SEARCH_INDEX_NAME,
        credential=__import__(
            "azure.core.credentials",
            fromlist=["AzureKeyCredential"],
        ).AzureKeyCredential(
            settings.AZURE_SEARCH_API_KEY,
        ),
    )

    search_service = AzureSearchSyncService()
    search_service.search_service.client = client

    results = client.search(
        search_text="*",
        select=["id", "document_id"],
    )

    chunk_ids = [
        result["id"]
        for result in results
        if result.get("document_id") in document_ids
    ]

    if chunk_ids:
        search_service.delete_documents(chunk_ids)

    print(f"Deleted {len(chunk_ids)} Azure Search test chunks.")


if __name__ == "__main__":
    asyncio.run(cleanup())