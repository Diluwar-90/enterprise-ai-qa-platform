from uuid import uuid4

import pytest

from app.services.document_storage import AzureBlobDocumentStorage


@pytest.mark.asyncio
async def test_azure_blob_storage_real_upload_download() -> None:
    storage = AzureBlobDocumentStorage(
        account_url="https://stenterpriseaiqa.blob.core.windows.net/",
        container_name="documents",
    )

    document_id = uuid4()
    filename = "integration-test.txt"
    content = b"Azure Blob Storage integration test"

    try:
        blob_path = await storage.save_file(
            content,
            document_id,
            filename,
        )

        downloaded_file = await storage.get_file(
            document_id,
            filename,
        )

        assert blob_path == f"documents/{document_id}/{filename}"
        assert downloaded_file.read_bytes() == content
    finally:
        blob_client = storage.container_client.get_blob_client(
            f"{document_id}/{filename}"
        )

        await blob_client.delete_blob()

        await storage.close()
