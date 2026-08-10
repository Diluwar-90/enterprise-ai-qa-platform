from openai import AsyncOpenAI

from app.core.config import get_settings


class LLMService:
    def __init__(self) -> None:
        settings = get_settings()

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
        )
        self.model = settings.OPENAI_MODEL

    async def generate(
        self,
        prompt: str,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""