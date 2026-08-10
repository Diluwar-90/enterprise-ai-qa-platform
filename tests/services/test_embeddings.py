from app.services.embeddings.service import EmbeddingService


def test_embed_text() -> None:
    service = EmbeddingService()

    embedding = service.embed_text(
        "Enterprise Knowledge Intelligence Platform"
    )

    assert len(embedding) == service.dimension
    assert len(embedding) > 0