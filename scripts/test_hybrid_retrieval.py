import asyncio

from app.services.retrieval import RetrievalService


async def main() -> None:
    service = RetrievalService()

    result = await service.retrieve_hybrid(
        query="What is the Enterprise Knowledge Intelligence Platform?",
        limit=5,
    )

    print("=== CONTEXT ===")
    print(result.context)

    print("\n=== SOURCES ===")
    for chunk in result.chunks:
        print(
            f"filename={chunk.document.filename} | "
            f"chunk_index={chunk.chunk_index}"
        )


if __name__ == "__main__":
    asyncio.run(main())