from app.agents.graph import build_agent_graph
from app.core.exceptions import AgentExecutionError


class AgentService:
    def __init__(self) -> None:
        self.graph = build_agent_graph()

    async def run(self, query: str) -> str:
        try:
            result = await self.graph.ainvoke(
                {
                    "query": query,
                }
            )

            return result["answer"]

        except Exception as exc:
            raise AgentExecutionError(
                "Agent execution failed."
            ) from exc