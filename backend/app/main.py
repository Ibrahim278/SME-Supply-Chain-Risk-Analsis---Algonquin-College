"""FastAPI application entry point."""

import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator, Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router
from app.core.logging import (
    clear_request_id,
    configure_logging,
    get_logger,
    set_request_id,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    configure_logging()
    logger = get_logger(__name__)
    logger.info("Starting SME Supply Chain Risk Analysis API")
    yield
    # Shutdown
    logger.info("Shutting down SME Supply Chain Risk Analysis API")


app = FastAPI(
    title="SME Supply Chain Risk Analysis API",
    description="API for analyzing supply chain risks for SME suppliers",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Add request ID to each request for correlation."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    set_request_id(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    clear_request_id()
    return response


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        dict with status "ok" indicating the service is healthy.
    """
    return {"status": "ok"}


# Mount API v1 router
app.include_router(api_v1_router, prefix="/api/v1")
