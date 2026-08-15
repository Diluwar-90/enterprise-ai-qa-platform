import asyncio

from app.services.azure_openai import AzureOpenAIService


async def main() -> None:
    service = AzureOpenAIService()

    answer = await service.generate(
        "In one sentence, what is the Enterprise Knowledge Intelligence Platform?"
    )

    print("=== AZURE OPENAI RESPONSE ===")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())