"""Health endpoint tests for the SME backend API."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Specify the async backend for pytest-asyncio."""
    return "asyncio"


@pytest.fixture
async def client() -> AsyncClient:
    """Create an async test client for the FastAPI application."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient) -> None:
    """Test that the health endpoint returns 200 OK."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_docs_endpoint(client: AsyncClient) -> None:
    """Test that the docs endpoint is accessible."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_openapi_endpoint(client: AsyncClient) -> None:
    """Test that the OpenAPI schema is available."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert data["info"]["title"] == "SME Supply Chain Risk Analysis API"
