from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import LLMService
from app.services.retrieval import RetrievalResult, RetrievalService


class RAGService:
    def __init__(self) -> None:
        self.retrieval = RetrievalService()
        self.llm = LLMService()

    async def answer(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ) -> tuple[str, RetrievalResult]:
        retrieval_result = await self.retrieval.retrieve(
            db=db,
            query=query,
            limit=limit,
        )
    
        prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using only the provided context.
If the context does not contain enough information, say that you
do not have enough information to answer.

Context:
{retrieval_result.context}

Question:
{query}
"""
        answer = await self.llm.generate(prompt)
        return answer, retrieval_result

    async def answer_hybrid(
        self,
        query: str,
        limit: int = 5,
    ) -> tuple[str, RetrievalResult]:
        retrieval_result = await self.retrieval.retrieve_hybrid(
            query=query,
            limit=limit,
        )

        prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using only the provided context.
If the context does not contain enough information, say that you
do not have enough information to answer.

Context:
{retrieval_result.context}

Question:
{query}
"""

        answer = await self.llm.generate(prompt)

        return answer, retrieval_result