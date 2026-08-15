from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.documents import router as documents_router
from app.api.rag import router as rag_router
from app.core.config import get_settings
from app.services.llm import LLMGenerationError

app = FastAPI(
    title=get_settings().APP_NAME,
    version=get_settings().APP_VERSION,
    description="Enterprise-grade GenAI platform with RAG and Agentic AI",
)

@app.exception_handler(LLMGenerationError)
async def llm_generation_error_handler(
    request: Request,
    exc: LLMGenerationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": "The language model service is temporarily unavailable."
        },
    )

app.include_router(documents_router)
app.include_router(rag_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": get_settings().APP_NAME,
        "version": get_settings().APP_VERSION,
    }
