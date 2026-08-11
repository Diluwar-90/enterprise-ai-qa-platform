from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import LLMService
from app.services.retrieval import RetrievalService


class RAGService:
    def __init__(self) -> None:
        self.retrieval = RetrievalService()
        self.llm = LLMService()

    async def answer(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 5,
    ) -> str:
        retrieval_result = await self.retrieval.retrieve(
            db=db,
            query=query,
            limit=limit,
        )
        context = retrieval_result.context

        prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using only the provided context.
If the context does not contain enough information, say that you
do not have enough information to answer.

Context:
{context}

Question:
{query}
"""

        return await self.llm.generate(prompt)