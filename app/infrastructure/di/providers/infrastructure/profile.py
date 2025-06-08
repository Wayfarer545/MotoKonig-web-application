# app/infrastructure/di/providers/infrastructure/profile.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.profile import IProfileRepository
from app.infrastructure.repositories.sql_profile_repo import SqlProfileRepository


class ProfileRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_profile_repo(self, session: AsyncSession) -> IProfileRepository:
        return SqlProfileRepository(session)
