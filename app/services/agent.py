from typing import Any

from app.agents.graph import build_agent_graph
from app.core.exceptions import AgentExecutionError


class AgentService:
    def __init__(self) -> None:
        self.graph = build_agent_graph()

    async def run(self, query: str) -> dict[str, Any]:
        try:
            result = await self.graph.ainvoke(
                {
                    "query": query,
                }
            )

            return {
                "answer": result.get("answer", ""),
                "approval_required": result.get(
                    "approval_required",
                    False,
                ),
                "approval_status": result.get(
                    "approval_status",
                    "not_required",
                ),
                "action": result.get("action"),
            }

        except Exception as exc:
            raise AgentExecutionError(
                "Agent execution failed."
            ) from exc