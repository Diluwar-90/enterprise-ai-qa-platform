import json
from typing import Any

from app.services.redis import RedisService


class ConversationMemoryService:
    TTL_SECONDS = 3600
    MAX_MESSAGES = 20

    def __init__(self) -> None:
        self.redis = RedisService()

    def _build_key(self, session_id: str) -> str:
        return f"conversation:memory:{session_id}"

    async def get_messages(
        self,
        session_id: str,
    ) -> list[dict[str, Any]]:
        value = await self.redis.get(
            self._build_key(session_id)
        )

        if value is None:
            return []

        return json.loads(value)

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        messages = await self.get_messages(session_id)

        messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        messages = messages[-self.MAX_MESSAGES :]

        await self.redis.set(
            self._build_key(session_id),
            json.dumps(messages),
            expire_seconds=self.TTL_SECONDS,
        )

    async def clear(self, session_id: str) -> None:
        await self.redis.delete(
            self._build_key(session_id)
        )

    async def close(self) -> None:
        await self.redis.close()