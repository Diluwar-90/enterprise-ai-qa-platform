from openai import AsyncAzureOpenAI, AsyncOpenAI

from app.core.config import get_settings


class LLMGenerationError(Exception):
    """Raised when the configured LLM provider fails to generate a response."""
    
class LLMService:
    def __init__(self) -> None:
        settings = get_settings()

        self.provider = settings.LLM_PROVIDER

        if self.provider == "azure":
            self.client = AsyncAzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_version=settings.AZURE_OPENAI_API_VERSION,
            )
            self.model = settings.AZURE_OPENAI_DEPLOYMENT
        else:
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
            )
            self.model = settings.OPENAI_MODEL

    async def generate(
        self,
        prompt: str,
    ) -> str:
        try:
            response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        except Exception as exc:
            raise LLMGenerationError(
                f"LLM generation failed using provider '{self.provider}'."
            ) from exc

        

        content =  response.choices[0].message.content or ""

        if not content:
            raise LLMGenerationError(
                f"LLM returned an empty response using provider '{self.provider}'."
        )

        return content
