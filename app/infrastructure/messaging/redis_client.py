# app/infrastructure/messaging/redis_client.py

from redis.asyncio import ConnectionPool, Redis

from app.config.settings import RedisConfig


class RedisClient:
    """Фабрика для создания Redis клиентов"""

    _pool: ConnectionPool | None = None

    @classmethod
    async def create_pool(cls, config: RedisConfig) -> None:
        """Создать пул соединений"""
        if cls._pool is None:
            cls._pool = ConnectionPool(
                host=config.redis_host,
                port=config.redis_port,
                decode_responses=True,
                max_connections=50
            )

    @classmethod
    async def get_client(cls) -> Redis:
        """Получить Redis клиент из пула"""
        if cls._pool is None:
            raise RuntimeError("Redis pool not initialized")
        return Redis(connection_pool=cls._pool)

    @classmethod
    async def close_pool(cls) -> None:
        """Закрыть пул соединений"""
        if cls._pool:
            await cls._pool.disconnect()
            cls._pool = None
