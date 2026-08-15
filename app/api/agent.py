from typing import Annotated

from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from fastapi import APIRouter, Depends

from app.services.agent import AgentService

router = APIRouter(prefix="/agent", tags=["Agent"])


def get_agent_service() -> AgentService:
    return AgentService()


@router.post(
    "/query",
    response_model=AgentQueryResponse,
)
async def query_agent(
    request: AgentQueryRequest,
    agent_service: Annotated[
        AgentService,
        Depends(get_agent_service),
    ],
) -> AgentQueryResponse:
    answer = await agent_service.run(request.query)

    return AgentQueryResponse(
        answer=answer,
    )                       