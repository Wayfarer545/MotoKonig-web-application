# app/infrastructure/di/providers/infrastructure/moto_club.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.moto_club import IMotoClubRepository
from app.infrastructure.repositories.sql_moto_club_repo import SqlMotoClubRepository


class MotoClubRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_moto_club_repo(self, session: AsyncSession) -> IMotoClubRepository:
        return SqlMotoClubRepository(session)
