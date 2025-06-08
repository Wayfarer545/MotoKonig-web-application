# app/infrastructure/di/providers/infrastructure/social_link.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.social_link import ISocialLinkRepository
from app.infrastructure.repositories.sql_social_link_repo import SqlSocialLinkRepository


class SocialLinkRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_social_link_repo(self, session: AsyncSession) -> ISocialLinkRepository:
        return SqlSocialLinkRepository(session)
