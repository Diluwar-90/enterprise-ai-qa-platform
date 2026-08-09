from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_async_session as get_db_session
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentResponse
from app.services.document_storage import LocalDocumentStorage

router = APIRouter(prefix="/documents", tags=["Documents"])

storage = LocalDocumentStorage(get_settings().DOCUMENT_STORAGE_PATH)

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post(
    "/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED
)
async def upload_document(
    file: Annotated[UploadFile, File(...)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}",
        )

    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE / (1024 * 1024)} MB",
        )

    document_id = uuid4()
    storage_path = await storage.save_file(
        file_content, document_id, file.filename or "document"
    )

    document = Document(
        id=document_id,
        owner_id=UUID("11111111-1111-1111-1111-111111111111"),  # Replace with actual user ID from authentication
        filename=file.filename or "document",
        content_type=file.content_type,
        file_size=len(file_content),
        status=DocumentStatus.UPLOADED,
        storage_path=storage_path,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    return document
