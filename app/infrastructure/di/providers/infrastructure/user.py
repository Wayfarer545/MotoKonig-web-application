# app/infrastructure/di/providers/infrastructure/user.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.user import IUserRepository
from app.infrastructure.repositories.sql_user_repo import SqlUserRepository


class UserRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_user_repo(self, session: AsyncSession) -> IUserRepository:
        return SqlUserRepository(session)
