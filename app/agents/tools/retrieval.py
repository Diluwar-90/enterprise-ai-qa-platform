from app.services.retrieval import RetrievalService


class RetrievalTool:
    name = "knowledge_search"
    description = (
        "Search enterprise knowledge and retrieve relevant document context."
    )

    def __init__(self) -> None:
        self.retrieval = RetrievalService()

    async def search(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        try:
            result = await self.retrieval.retrieve_hybrid(
                query=query,
                limit=limit,
            )

            return result.context
        except Exception as exc:
            raise RuntimeError(
                "Retrieval tool failed."
            ) from exc