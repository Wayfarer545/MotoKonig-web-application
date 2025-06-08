from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from dishka import Provider, Scope, provide
from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Config
from app.infrastructure.messaging.redis_client import RedisClient


class InfrastructureBaseProvider(Provider):
    def __init__(self, alchemy: AdvancedAlchemy, config: Config) -> None:
        Provider.__init__(self)
        self.alchemy = alchemy
        self.config = config

    @provide(scope=Scope.REQUEST)
    def provide_db_session(self, request: Request) -> AsyncSession:
        """Get DB session from Advanced-Alchemy."""
        return self.alchemy.get_session(request)

    @provide(scope=Scope.APP)
    async def provide_redis(self) -> Redis:
        """Provide Redis client."""
        await RedisClient.create_pool(self.config.redis)
        return await RedisClient.get_client()
