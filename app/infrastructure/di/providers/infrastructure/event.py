# app/infrastructure/di/providers/infrastructure/event.py
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.event import IEventRepository
from app.domain.ports.repositories.event_participation import (
    IEventParticipationRepository,
)
from app.infrastructure.repositories.sql_event_participation_repo import (
    SqlEventParticipationRepository,
)
from app.infrastructure.repositories.sql_event_repo import SqlEventRepository


class EventRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_event_repo(self, session: AsyncSession) -> IEventRepository:
        return SqlEventRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_event_participation_repo(
            self, session: AsyncSession
    ) -> IEventParticipationRepository:
        return SqlEventParticipationRepository(session)