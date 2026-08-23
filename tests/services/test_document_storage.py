from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.services.document_storage import (
    AzureBlobDocumentStorage,
    LocalDocumentStorage,
    create_document_storage,
)


@pytest.mark.asyncio
async def test_local_storage_save_and_get(tmp_path: Path) -> None:
    storage = LocalDocumentStorage(str(tmp_path))
    document_id = uuid4()
    filename = "test.txt"
    content = b"Enterprise Knowledge Intelligence Platform"

    storage_path = await storage.save_file(
        content,
        document_id,
        filename,
    )

    file_path = await storage.get_file(
        document_id,
        filename,
    )

    assert storage_path == str(file_path)
    assert file_path.read_bytes() == content


@pytest.mark.asyncio
async def test_local_storage_missing_file(tmp_path: Path) -> None:
    storage = LocalDocumentStorage(str(tmp_path))

    with pytest.raises(FileNotFoundError):
        await storage.get_file(
            uuid4(),
            "missing.txt",
        )


def test_create_document_storage_defaults_to_local(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("DOCUMENT_STORAGE_PROVIDER", "local")
    monkeypatch.setenv(
        "DOCUMENT_STORAGE_PATH",
        str(tmp_path),
    )

    storage = create_document_storage()

    assert isinstance(storage, LocalDocumentStorage)


@pytest.mark.asyncio
async def test_azure_blob_storage_save() -> None:
    storage = AzureBlobDocumentStorage(
        account_url="https://testaccount.blob.core.windows.net",
        container_name="documents",
    )

    blob_client = MagicMock()
    blob_client.upload_blob = AsyncMock()

    storage.container_client.get_blob_client = MagicMock(
        return_value=blob_client
    )

    document_id = uuid4()

    result = await storage.save_file(
        b"test content",
        document_id,
        "test.txt",
    )

    blob_client.upload_blob.assert_awaited_once_with(
        b"test content",
        overwrite=True,
    )

    assert result == f"documents/{document_id}/test.txt"

    await storage.close()