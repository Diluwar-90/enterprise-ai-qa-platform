from types import SimpleNamespace

from app.services.context_builder import ContextBuilder


def test_context_builder() -> None:
    chunks = [
        SimpleNamespace(chunk_index=0, content="First chunk."),
        SimpleNamespace(chunk_index=1, content="Second chunk."),
    ]

    result = ContextBuilder().build(chunks)

    assert "[Chunk 0]" in result
    assert "First chunk." in result
    assert "[Chunk 1]" in result
    assert "Second chunk." in result