import json
from typing import Any

from app.agents.graph import build_agent_graph
from app.core.exceptions import AgentExecutionError
from app.services.agent_cache import AgentCache
from app.services.conversation_memory import ConversationMemoryService
from app.services.redis import RedisService


class AgentService:
    def __init__(self) -> None:
        self.graph = build_agent_graph()
        self.redis = RedisService()
        self.conversation_memory = ConversationMemoryService()

    async def run(
        self,
        query: str,
        session_id: str,
    ) -> dict[str, Any]:
        cache_key = AgentCache.build_key(query)

        try:
            try:
                conversation = (
                    await self.conversation_memory.get_messages(
                        session_id
                    )
                )

                cached = await self.redis.get(cache_key)
            except ConnectionError:
                conversation = []
                cached = None

            if cached is not None:
                return json.loads(cached)

            result = await self.graph.ainvoke(
                {
                    "query": query,
                    "conversation": conversation,
                }
            )

            response = {
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

            await self.conversation_memory.add_message(
                session_id=session_id,
                role="user",
                content=query,
            )

            await self.conversation_memory.add_message(
                session_id=session_id,
                role="assistant",
                content=response["answer"],
            )

            if AgentCache.should_cache(response):
                try:
                    await self.redis.set(
                        cache_key,
                        json.dumps(response),
                        expire_seconds=AgentCache.TTL_SECONDS,
                    )
                except ConnectionError:
                    pass

            return response

        except Exception as exc:
            raise AgentExecutionError(
                "Agent execution failed."
            ) from exc