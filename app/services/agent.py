from app.agents.graph import build_agent_graph


class AgentService:
    def __init__(self) -> None:
        self.graph = build_agent_graph()

    async def run(self, query: str) -> str:
        result = await self.graph.ainvoke(
            {
                "query": query,
            }
        )

        return result["answer"]