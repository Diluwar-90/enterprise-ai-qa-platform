from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session as get_db_session
from app.schemas.rag import RAGQueryRequest, RAGQueryResponse, RAGSource
from app.services.rag import RAGService

router = APIRouter(prefix="/rag", tags=["RAG"])

def get_rag_service() -> RAGService:
    return RAGService()  


@router.post("/query",response_model=RAGQueryResponse)
async def query_rag(
    request: RAGQueryRequest,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    rag_service: Annotated[RAGService, Depends(get_rag_service)],
) -> RAGQueryResponse:
    answer, retrieval_result = await rag_service.answer(
        db=db,
        query=request.query,
    )

    sources = [
    RAGSource(
        document_id=chunk.document_id,
        filename=chunk.document.filename,
        chunk_index=chunk.chunk_index,
    )
    for chunk in retrieval_result.chunks
    ]

    return RAGQueryResponse(
    answer=answer,
    sources=sources,
    )