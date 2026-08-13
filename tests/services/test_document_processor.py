from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.models.user import User
from app.services.document_processor import DocumentProcessor


@pytest.mark.asyncio
async def test_process_text_document(
    tmp_path: Path,
    db_session: AsyncSession,
) -> None:
    user = User(
        id=uuid4(),
        email=f"test-{uuid4()}@example.com",
        full_name="Test User",
    )

    db_session.add(user)
    await db_session.commit()

    file_path = tmp_path / "test.txt"
    file_path.write_text(
        "Enterprise Knowledge Intelligence Platform test content.",
        encoding="utf-8",
    )

    document = Document(
        id=uuid4(),
        owner_id=user.id,
        filename="test.txt",
        content_type="text/plain",
        file_size=file_path.stat().st_size,
        status=DocumentStatus.UPLOADED,
        storage_path=str(file_path),
    )

    db_session.add(document)
    await db_session.commit()

    processor = DocumentProcessor()
    processor.azure_search_sync.upload_document = MagicMock()

    chunks = await processor.process(
        document=document,
        db=db_session,
    )

    assert document.status == DocumentStatus.PROCESSED
    assert len(chunks) > 0
    assert chunks[0].document_id == document.id
    assert chunks[0].content == (
        "Enterprise Knowledge Intelligence Platform test content."
    )
    assert processor.azure_search_sync.upload_document.call_count == len(chunks)