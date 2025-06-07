# app/infrastructure/repositories/sql_club_membership_repo.py

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.club_membership import ClubMembership
from app.domain.ports.repositories.club_membership import (
    IClubMembershipRepository,
)
from app.domain.ports.specs.club_membership import (
    ClubMembershipSpecificationPort,
)
from app.domain.value_objects.club_role import ClubRole
from app.infrastructure.models.club_membership import (
    ClubMembership as ClubMembershipModel,
)


class SqlClubMembershipRepository(IClubMembershipRepository):
    """SQLAlchemy реализация репозитория членства в мотоклубах"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, membership: ClubMembership) -> ClubMembership:
        """Добавить новое членство"""
        db_membership = ClubMembershipModel(
            club_id=membership.club_id,
            user_id=membership.user_id,
            role=membership.role,
            status=membership.status,
            joined_at=membership.joined_at.isoformat(),
            invited_by=membership.invited_by,
            notes=membership.notes,
        )

        self.session.add(db_membership)
        await self.session.flush()
        await self.session.refresh(db_membership)

        # Обновляем доменную сущность
        membership.id = db_membership.id
        membership.created_at = db_membership.created_at
        membership.updated_at = db_membership.updated_at

        return membership

    async def get(self, spec: ClubMembershipSpecificationPort) -> ClubMembership | None:
        """Получить членство по спецификации"""
        statement = spec.to_query(select(ClubMembershipModel))
        result = await self.session.execute(statement)
        db_membership = result.scalar_one_or_none()

        if db_membership:
            return self._to_domain_entity(db_membership)
        return None

    async def get_list(self, spec: ClubMembershipSpecificationPort | None = None) -> list[ClubMembership]:
        """Получить список членств по спецификации"""
        statement = select(ClubMembershipModel)

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        memberships = result.scalars().all()

        return [self._to_domain_entity(m) for m in memberships]

    async def update(self, membership: ClubMembership) -> ClubMembership:
        """Обновить членство"""
        db_membership = await self.session.get(ClubMembershipModel, membership.id)

        if db_membership:
            # Обновляем поля
            db_membership.role = membership.role
            db_membership.status = membership.status
            db_membership.notes = membership.notes

            await self.session.flush()
            await self.session.refresh(db_membership)

            # Обновляем timestamp в доменной сущности
            membership.updated_at = db_membership.updated_at

        return membership

    async def delete(self, membership_id: UUID) -> bool:
        """Удалить членство"""
        db_membership = await self.session.get(ClubMembershipModel, membership_id)

        if db_membership:
            await self.session.delete(db_membership)
            await self.session.flush()
            return True

        return False

    async def get_user_membership_in_club(self, user_id: UUID, club_id: UUID) -> ClubMembership | None:
        """Получить членство пользователя в конкретном клубе"""
        statement = select(ClubMembershipModel).where(
            ClubMembershipModel.user_id == user_id,
            ClubMembershipModel.club_id == club_id
        )
        result = await self.session.execute(statement)
        db_membership = result.scalar_one_or_none()

        if db_membership:
            return self._to_domain_entity(db_membership)
        return None

    async def count_club_members(self, club_id: UUID, active_only: bool = True) -> int:
        """Подсчитать количество участников клуба"""
        statement = select(func.count(ClubMembershipModel.id)).where(
            ClubMembershipModel.club_id == club_id
        )

        if active_only:
            statement = statement.where(ClubMembershipModel.status == "active")

        result = await self.session.execute(statement)
        return result.scalar() or 0

    def _to_domain_entity(self, db_membership: ClubMembershipModel) -> ClubMembership:
        """Преобразовать модель БД в доменную сущность"""
        from datetime import datetime

        joined_at = datetime.fromisoformat(db_membership.joined_at)

        return ClubMembership(
            membership_id=db_membership.id,
            club_id=db_membership.club_id,
            user_id=db_membership.user_id,
            role=ClubRole(db_membership.role.value),
            status=db_membership.status,
            joined_at=joined_at,
            invited_by=db_membership.invited_by,
            notes=db_membership.notes,
            created_at=db_membership.created_at,
            updated_at=db_membership.updated_at
        )
