from openai import AsyncAzureOpenAI

from app.core.config import get_settings


class AzureOpenAIService:
    def __init__(self) -> None:
        settings = get_settings()

        self.client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )

        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT

    async def generate(
        self,
        prompt: str,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""