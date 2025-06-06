# app/infrastructure/repositories/sql_moto_club_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.moto_club import MotoClub
from app.domain.ports.moto_club_repository import IMotoClubRepository
from app.domain.ports.moto_club_specification import MotoClubSpecificationPort
from app.infrastructure.models.moto_club_model import MotoClub as MotoClubModel


class SqlMotoClubRepository(IMotoClubRepository):
    """SQLAlchemy реализация репозитория мотоклубов"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, club: MotoClub) -> MotoClub:
        """Добавить новый мотоклуб"""
        db_club = MotoClubModel(
            name=club.name,
            description=club.description,
            president_id=club.president_id,
            is_public=club.is_public,
            max_members=club.max_members,
            location=club.location,
            website=club.website,
            avatar_url=club.avatar_url,
            is_active=club.is_active,
            founded_date=club.founded_date.isoformat() if club.founded_date else None,
        )

        self.session.add(db_club)
        await self.session.flush()
        await self.session.refresh(db_club)

        # Обновляем доменную сущность
        club.id = db_club.id
        club.created_at = db_club.created_at
        club.updated_at = db_club.updated_at

        return club

    async def get(self, spec: MotoClubSpecificationPort) -> MotoClub | None:
        """Получить мотоклуб по спецификации"""
        statement = spec.to_query(
            select(MotoClubModel).options(
                selectinload(MotoClubModel.memberships),
                selectinload(MotoClubModel.invitations)
            )
        )
        result = await self.session.execute(statement)
        db_club = result.scalar_one_or_none()

        if db_club:
            return self._to_domain_entity(db_club)
        return None

    async def get_list(self, spec: MotoClubSpecificationPort | None = None) -> list[MotoClub]:
        """Получить список мотоклубов по спецификации"""
        statement = select(MotoClubModel).options(
            selectinload(MotoClubModel.memberships),
            selectinload(MotoClubModel.invitations)
        )

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        clubs = result.scalars().all()

        return [self._to_domain_entity(club) for club in clubs]

    async def update(self, club: MotoClub) -> MotoClub:
        """Обновить мотоклуб"""
        db_club = await self.session.get(MotoClubModel, club.id)

        if db_club:
            # Обновляем поля
            db_club.name = club.name
            db_club.description = club.description
            db_club.president_id = club.president_id
            db_club.is_public = club.is_public
            db_club.max_members = club.max_members
            db_club.location = club.location
            db_club.website = club.website
            db_club.avatar_url = club.avatar_url
            db_club.is_active = club.is_active
            db_club.founded_date = club.founded_date.isoformat() if club.founded_date else None

            await self.session.flush()
            await self.session.refresh(db_club)

            # Обновляем timestamp в доменной сущности
            club.updated_at = db_club.updated_at

        return club

    async def delete(self, club_id: UUID) -> bool:
        """Удалить мотоклуб"""
        db_club = await self.session.get(MotoClubModel, club_id)

        if db_club:
            await self.session.delete(db_club)
            await self.session.flush()
            return True

        return False

    def _to_domain_entity(self, db_club: MotoClubModel) -> MotoClub:
        """Преобразовать модель БД в доменную сущность"""
        from datetime import datetime

        founded_date = None
        if db_club.founded_date:
            try:
                founded_date = datetime.fromisoformat(db_club.founded_date)
            except ValueError:
                founded_date = None

        return MotoClub(
            club_id=db_club.id,
            name=db_club.name,
            description=db_club.description,
            president_id=db_club.president_id,
            is_public=db_club.is_public,
            max_members=db_club.max_members,
            location=db_club.location,
            website=db_club.website,
            founded_date=founded_date,
            avatar_url=db_club.avatar_url,
            is_active=db_club.is_active,
            created_at=db_club.created_at,
            updated_at=db_club.updated_at
        )
