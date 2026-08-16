from typing import Literal

from pydantic import BaseModel, Field


class AgentQueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)


class AgentQueryResponse(BaseModel):
    answer: str
    request_id: str
    approval_required: bool = False
    approval_status: Literal[
        "not_required",
        "pending",
        "approved",
        "rejected",
    ] = "not_required"
    action: str | None = None