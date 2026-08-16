import logging
from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse

from app.services.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


async def add_request_id(request: Request, call_next):
    request_id = request.headers.get(
        "X-Request-ID",
        str(uuid4()),
    )

    request.state.request_id = request_id

    logger.info(
        "Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "Request completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
        },
    )

    return response

async def rate_limit_request(request: Request, call_next):
    rate_limiter = RateLimiter()

    client_key = request.client.host if request.client else "unknown"

    allowed = await rate_limiter.is_allowed(client_key)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded. Please try again later.",
            },
        )

    return await call_next(request)