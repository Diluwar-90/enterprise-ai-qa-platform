from app.services.chunking import DocumentChunker


def test_document_chunking() -> None:
    text = (
        "Enterprise AI systems require reliable retrieval. "
        * 100
    )

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.split(text)

    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)