# app/infrastructure/di/providers/infrastructure/motorcycle.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.motorcycle import IMotorcycleRepository
from app.infrastructure.repositories.sql_motorcycle_repo import SqlMotorcycleRepository


class MotorcycleRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_motorcycle_repo(self, session: AsyncSession) -> IMotorcycleRepository:
        return SqlMotorcycleRepository(session)
