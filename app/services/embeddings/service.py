from app.services.embeddings.local import LocalEmbeddingProvider


class EmbeddingService:
    def __init__(self) -> None:
        self.provider = LocalEmbeddingProvider()

    def embed_text(self, text: str) -> list[float]:
        return self.provider.embed_text(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.provider.embed_documents(texts)

    @property
    def dimension(self) -> int:
        return self.provider.dimension