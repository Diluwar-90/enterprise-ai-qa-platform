from app.core.config import get_settings
from app.services.redis import RedisService


class RateLimiter:
    PREFIX = "rate_limit:"

    def __init__(self) -> None:
        self.redis = RedisService()
        settings = get_settings()

        self.max_requests = settings.RATE_LIMIT_REQUESTS
        self.window_seconds = settings.RATE_LIMIT_WINDOW_SECONDS

    async def is_allowed(self, client_key: str) -> bool:
        key = f"{self.PREFIX}{client_key}"

        current = await self.redis.get(key)

        if current is None:
            await self.redis.set(
                key,
                "1",
                expire_seconds=self.window_seconds,
            )
            return True

        request_count = int(current)

        if request_count >= self.max_requests:
            return False

        await self.redis.set(
            key,
            str(request_count + 1),
            expire_seconds=self.window_seconds,
        )

        return True