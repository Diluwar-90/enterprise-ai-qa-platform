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

        if not retrieval_result.chunks:
            return (
            "I do not have enough information to answer.",
            retrieval_result,
            )
    
        prompt = f"""
You are an enterprise knowledge assistant.

Your job is to answer the user's question using ONLY the information
provided in the context below.

Rules:
1. Do not use information that is not present in the context.
2. Do not invent or assume facts.
3. If the context does not contain enough information to answer the
   question, respond exactly:
   "I do not have enough information to answer."
4. Give a clear and concise answer.
5. When the context contains relevant technical details, preserve
   their meaning accurately.

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

        if not retrieval_result.chunks:
            return (
            "I do not have enough information to answer.",
            retrieval_result,
        )

        prompt = f"""
You are an enterprise knowledge assistant.

Your job is to answer the user's question using ONLY the information
provided in the context below.

Rules:
1. Do not use information that is not present in the context.
2. Do not invent or assume facts.
3. If the context does not contain enough information to answer the
   question, respond exactly:
   "I do not have enough information to answer."
4. Give a clear and concise answer.
5. When the context contains relevant technical details, preserve
   their meaning accurately.

Context:
{retrieval_result.context}

Question:
{query}
"""

        answer = await self.llm.generate(prompt)

        return answer, retrieval_result