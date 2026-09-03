import os
from uuid import uuid4

import pytest

from app.services.document_storage import AzureBlobDocumentStorage


@pytest.mark.asyncio
@pytest.mark.skipif(
    os.getenv("RUN_AZURE_BLOB_INTEGRATION") != "true",
    reason="Azure Blob integration test is disabled.",
)
async def test_azure_blob_storage_real_upload_download() -> None:
    account_url = os.getenv("AZURE_BLOB_STORAGE_ACCOUNT_URL")

    if not account_url:
        pytest.fail(
            "AZURE_BLOB_STORAGE_ACCOUNT_URL must be set "
            "when Azure Blob integration testing is enabled."
        )

    container_name = os.getenv(
        "AZURE_BLOB_STORAGE_CONTAINER",
        "documents",
    )

    storage = AzureBlobDocumentStorage(
        account_url=account_url,
        container_name=container_name,
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

        assert blob_path == f"{container_name}/{document_id}/{filename}"
        assert downloaded_file.read_bytes() == content

    finally:
        blob_client = storage.container_client.get_blob_client(
            f"{document_id}/{filename}"
        )

        await blob_client.delete_blob()
        await storage.close()