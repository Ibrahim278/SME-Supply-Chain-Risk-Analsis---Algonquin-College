"""Redis configuration and client management."""

from collections.abc import AsyncGenerator

import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings

# Create connection pool for efficient connection reuse
redis_pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    max_connections=10,
)


async def get_redis() -> AsyncGenerator[Redis, None]:
    """Dependency for getting async Redis client.

    Usage in FastAPI:
        @app.get("/cache")
        async def get_cache(redis_client: Redis = Depends(get_redis)):
            value = await redis_client.get("key")
            ...
    """
    client = redis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.aclose()


async def check_redis_health() -> bool:
    """Check if Redis is reachable and responsive."""
    client = redis.Redis(connection_pool=redis_pool)
    try:
        return await client.ping()
    except Exception:
        return False
    finally:
        await client.aclose()
