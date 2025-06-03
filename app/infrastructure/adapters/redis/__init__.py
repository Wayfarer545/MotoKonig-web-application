# app/infrastructure/adapters/redis/__init__.py

from .client import create_redis_client

__all__ = ["create_redis_client"]
