import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.agent import router as agent_router
from app.api.documents import router as documents_router
from app.api.rag import router as rag_router
from app.core.config import get_settings
from app.core.exceptions import AgentExecutionError
from app.core.middleware import add_request_id
from app.services.llm import LLMGenerationError

logger = logging.getLogger(__name__)

app = FastAPI(
    title=get_settings().APP_NAME,
    version=get_settings().APP_VERSION,
    description="Enterprise-grade GenAI platform with RAG and Agentic AI",
)
app.middleware("http")(add_request_id)

@app.exception_handler(LLMGenerationError)
async def llm_generation_error_handler(
    request: Request,
    exc: LLMGenerationError,
) -> JSONResponse:
    logger.exception(
        "LLM generation failed",
        extra={
            "request_id": request.state.request_id,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=503,
        content={
            "detail": "The language model service is temporarily unavailable."
        },
    )

@app.exception_handler(AgentExecutionError)
async def agent_execution_error_handler(
    request: Request,
    exc: AgentExecutionError,
) -> JSONResponse:
    logger.exception(
        "Agent execution failed",
        extra={
            "request_id": request.state.request_id,
            "path": request.url.path,
            "method": request.method,
        },
    )
    
    return JSONResponse(
        status_code=503,
        content={
            "detail": "The agent service is temporarily unavailable."
        },
    )   

app.include_router(documents_router)
app.include_router(rag_router)
app.include_router(agent_router)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": get_settings().APP_NAME,
        "version": get_settings().APP_VERSION,
    }
