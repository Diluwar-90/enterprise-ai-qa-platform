import json
from typing import Any

from app.services.redis import RedisService


class MemoryService:
    SHORT_TERM_TTL_SECONDS = 3600
    SHORT_TERM_PREFIX = "memory:short"
    LONG_TERM_PREFIX = "memory:long"

    def __init__(self) -> None:
        self.redis = RedisService()

    def _short_term_key(self, session_id: str) -> str:
        return f"{self.SHORT_TERM_PREFIX}:{session_id}"

    def _long_term_key(self, user_id: str) -> str:
        return f"{self.LONG_TERM_PREFIX}:{user_id}"

    async def add_short_term(
        self,
        session_id: str,
        query: str,
        answer: str,
    ) -> None:
        key = self._short_term_key(session_id)

        existing = await self.redis.get(key)

        messages: list[dict[str, Any]] = []

        if existing:
            messages = json.loads(existing)

        messages.append(
            {
                "query": query,
                "answer": answer,
            }
        )

        # Keep recent conversation bounded.
        messages = messages[-10:]

        await self.redis.set(
            key,
            json.dumps(messages),
            expire_seconds=self.SHORT_TERM_TTL_SECONDS,
        )

    async def get_short_term(
        self,
        session_id: str,
    ) -> list[dict[str, Any]]:
        value = await self.redis.get(
            self._short_term_key(session_id)
        )

        if not value:
            return []

        return json.loads(value)

    async def add_long_term(
        self,
        user_id: str,
        memory: dict[str, Any],
    ) -> None:
        key = self._long_term_key(user_id)

        existing = await self.redis.get(key)

        memories: list[dict[str, Any]] = []

        if existing:
            memories = json.loads(existing)

        memories.append(memory)

        await self.redis.set(
            key,
            json.dumps(memories),
        )

    async def get_long_term(
        self,
        user_id: str,
    ) -> list[dict[str, Any]]:
        value = await self.redis.get(
            self._long_term_key(user_id)
        )

        if not value:
            return []

        return json.loads(value)