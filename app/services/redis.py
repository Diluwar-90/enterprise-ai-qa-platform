from redis.asyncio import Redis

from app.core.config import get_settings


class RedisService:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    async def set(
        self,
        key: str,
        value: str,
        expire_seconds: int | None = None,
    ) -> None:
        await self.client.set(
            key,
            value,
            ex=expire_seconds,
        )

    async def get(self, key: str) -> str | None:
        return await self.client.get(key)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def close(self) -> None:
        await self.client.aclose()