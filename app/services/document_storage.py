from pathlib import Path
from uuid import UUID


class LocalDocumentStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_file(
        self, file_content: bytes, document_id: UUID, filename: str
    ) -> str:
        document_directory = self.base_path / str(document_id)
        document_directory.mkdir(parents=True, exist_ok=True)
        file_path = document_directory / filename
        file_path.write_bytes(file_content)
        return str(file_path)

    async def get_file(self, document_id: UUID, filename: str) -> Path:
        file_path = self.base_path / str(document_id) / filename
        if not file_path.exists():
            raise FileNotFoundError("File not found.")
        return file_path
