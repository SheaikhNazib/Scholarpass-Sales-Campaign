"""Redis client configuration and utilities."""

import redis
from src.config import get_settings
from typing import Optional, Any

settings = get_settings()

# Redis client instance
redis_client: Optional[redis.Redis] = None

def get_redis_client() -> redis.Redis:
    """Get or create Redis client."""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return redis_client

def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client:
        redis_client.close()
        redis_client = None

async def get_cached(key: str) -> Optional[Any]:
    """Get value from cache."""
    client = get_redis_client()
    return client.get(key)

async def set_cached(key: str, value: Any, ttl: int = 3600) -> bool:
    """Set value in cache with TTL."""
    client = get_redis_client()
    return client.setex(key, ttl, value)

async def delete_cached(key: str) -> bool:
    """Delete value from cache."""
    client = get_redis_client()
    return bool(client.delete(key))

async def clear_cache() -> None:
    """Clear all cache."""
    client = get_redis_client()
    client.flushdb()
