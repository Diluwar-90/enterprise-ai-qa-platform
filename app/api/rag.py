from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session as get_db_session
from app.services.rag import RAGService

router = APIRouter(prefix="/rag", tags=["RAG"])

def get_rag_service() -> RAGService:
    return RAGService()  


@router.post("/query")
async def query_rag(
    query: str,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    rag_service: Annotated[RAGService, Depends(get_rag_service)],
) -> dict[str, str]:
    answer = await rag_service.answer(
        db=db,
        query=query,
    )

    return {"answer": answer}