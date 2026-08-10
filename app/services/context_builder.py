from app.models.document_chunk import DocumentChunk


class ContextBuilder:
    def build(self, chunks: list[DocumentChunk]) -> str:
        return "\n\n".join(
            f"[Chunk {chunk.chunk_index}]\n{chunk.content}"
            for chunk in chunks
        )