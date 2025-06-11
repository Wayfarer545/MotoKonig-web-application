# app/infrastructure/di/providers/infrastructure/motokonig.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.achievement import IAchievementRepository
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.domain.ports.repositories.ride import IRideRepository
from app.infrastructure.repositories.sql_achievement_repo import (
    SqlAchievementRepository,
)
from app.infrastructure.repositories.sql_motokonig_repo import SqlMotoKonigRepository
from app.infrastructure.repositories.sql_ride_repo import SqlRideRepository

__all__ = ["MotoKonigRepoProvider"]


class MotoKonigRepoProvider(Provider):
    """DI провайдер для MotoKonig репозиториев"""

    @provide(scope=Scope.REQUEST)
    def provide_motokonig_repo(self, session: AsyncSession) -> IMotoKonigRepository:
        return SqlMotoKonigRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_ride_repo(self, session: AsyncSession) -> IRideRepository:
        return SqlRideRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_achievement_repo(self, session: AsyncSession) -> IAchievementRepository:
        return SqlAchievementRepository(session)
