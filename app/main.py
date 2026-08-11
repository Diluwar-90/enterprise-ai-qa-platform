from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.api.rag import router as rag_router
from app.core.config import get_settings

app = FastAPI(
    title=get_settings().APP_NAME,
    version=get_settings().APP_VERSION,
    description="Enterprise-grade GenAI platform with RAG and Agentic AI",
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
