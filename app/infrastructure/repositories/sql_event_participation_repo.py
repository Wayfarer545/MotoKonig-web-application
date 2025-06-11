# app/infrastructure/repositories/sql_event_participation_repo.py
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.event_participation import EventParticipation
from app.domain.ports.repositories.event_participation import (
    IEventParticipationRepository,
)
from app.infrastructure.models.event_participation import (
    EventParticipation as EventParticipationModel,
)


class SqlEventParticipationRepository(IEventParticipationRepository):
    """SQLAlchemy реализация репозитория участий"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, participation: EventParticipation) -> EventParticipation:
        db_part = EventParticipationModel(
            event_id=participation.event_id,
            user_id=participation.user_id,
            joined_at=participation.joined_at,
        )
        self.session.add(db_part)
        await self.session.flush()
        await self.session.refresh(db_part)

        participation.id = db_part.id
        participation.created_at = db_part.created_at
        participation.updated_at = db_part.updated_at
        return participation

    async def get(self, event_id: UUID, user_id: UUID) -> EventParticipation | None:
        statement = select(EventParticipationModel).where(
            EventParticipationModel.event_id == str(event_id),
            EventParticipationModel.user_id == str(user_id),
            )
        result = await self.session.execute(statement)
        db_part = result.scalar_one_or_none()
        if db_part:
            return self._to_domain_entity(db_part)
        return None

    async def list_for_event(self, event_id: UUID) -> list[EventParticipation]:
        statement = select(EventParticipationModel).where(
            EventParticipationModel.event_id == str(event_id)
        )
        result = await self.session.execute(statement)
        parts = result.scalars().all()
        return [self._to_domain_entity(p) for p in parts]

    async def delete(self, event_id: UUID, user_id: UUID) -> bool:
        statement = select(EventParticipationModel).where(
            EventParticipationModel.event_id == str(event_id),
            EventParticipationModel.user_id == str(user_id),
            )
        result = await self.session.execute(statement)
        db_part = result.scalar_one_or_none()
        if db_part:
            await self.session.delete(db_part)
            await self.session.flush()
            return True
        return False

    async def count_for_event(self, event_id: UUID) -> int:
        statement = select(EventParticipationModel).where(
            EventParticipationModel.event_id == str(event_id)
        )
        result = await self.session.execute(statement)
        return len(result.scalars().all())

    def _to_domain_entity(self, db_part: EventParticipationModel) -> EventParticipation:
        return EventParticipation(
            participation_id=db_part.id,
            event_id=db_part.event_id,
            user_id=db_part.user_id,
            joined_at=db_part.joined_at,
            created_at=db_part.created_at,
            updated_at=db_part.updated_at,
        )