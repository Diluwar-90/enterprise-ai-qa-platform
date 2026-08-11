from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RAGQueryRequest(BaseModel):
    query: str = Field(min_length=1)

class RAGSource(BaseModel):
    document_id: UUID
    filename: str
    chunk_index: int

    model_config = ConfigDict(from_attributes=True)

class RAGQueryResponse(BaseModel):
    answer: str
    sources: list[RAGSource]