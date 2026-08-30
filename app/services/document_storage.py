from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Protocol
from uuid import UUID

from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

from app.core.config import get_settings


class DocumentStorage(Protocol):
    async def save_file(
        self,
        file_content: bytes,
        document_id: UUID,
        filename: str,
    ) -> str:
        ...

    async def get_file(
        self,
        document_id: UUID,
        filename: str,
    ) -> Path:
        ...


class LocalDocumentStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_file(
        self,
        file_content: bytes,
        document_id: UUID,
        filename: str,
    ) -> str:
        document_directory = self.base_path / str(document_id)
        document_directory.mkdir(parents=True, exist_ok=True)

        file_path = document_directory / filename
        file_path.write_bytes(file_content)

        return str(file_path)

    async def get_file(
        self,
        document_id: UUID,
        filename: str,
    ) -> Path:
        file_path = self.base_path / str(document_id) / filename

        if not file_path.exists():
            raise FileNotFoundError("File not found.")

        return file_path


class AzureBlobDocumentStorage:
    def __init__(
        self,
        account_url: str,
        container_name: str,
    ):
        self.account_url = account_url
        self.container_name = container_name

        self.credential = DefaultAzureCredential()

        self.client = BlobServiceClient(
            account_url=account_url,
            credential=self.credential,
        )

        self.container_client = self.client.get_container_client(
            container_name
        )

    def _blob_name(
        self,
        document_id: UUID,
        filename: str,
    ) -> str:
        return f"{document_id}/{filename}"

    async def save_file(
        self,
        file_content: bytes,
        document_id: UUID,
        filename: str,
    ) -> str:
        blob_name = self._blob_name(
            document_id,
            filename,
        )

        blob_client = self.container_client.get_blob_client(
            blob_name
        )

        await blob_client.upload_blob(
            file_content,
            overwrite=True,
        )

        return f"{self.container_name}/{blob_name}"

    async def get_file(
        self,
        document_id: UUID,
        filename: str,
    ) -> Path:
        blob_name = self._blob_name(
            document_id,
            filename,
        )

        blob_client = self.container_client.get_blob_client(
            blob_name
        )

        if not await blob_client.exists():
            raise FileNotFoundError("File not found.")

        download = await blob_client.download_blob()
        content = await download.readall()

        with NamedTemporaryFile(delete=False) as temporary_file:
            temporary_file.write(content)
            temporary_file_path = Path(temporary_file.name)

        return temporary_file_path

    async def close(self) -> None:
        await self.client.close()
        await self.credential.close()


def create_document_storage() -> DocumentStorage:
    settings = get_settings()

    if settings.DOCUMENT_STORAGE_PROVIDER == "azure_blob":
        if not settings.AZURE_BLOB_STORAGE_ACCOUNT_URL:
            raise ValueError(
                "AZURE_BLOB_STORAGE_ACCOUNT_URL is required "
                "when using Azure Blob Storage."
            )

        return AzureBlobDocumentStorage(
            account_url=settings.AZURE_BLOB_STORAGE_ACCOUNT_URL,
            container_name=settings.AZURE_BLOB_STORAGE_CONTAINER,
        )

    return LocalDocumentStorage(
        settings.DOCUMENT_STORAGE_PATH
    )