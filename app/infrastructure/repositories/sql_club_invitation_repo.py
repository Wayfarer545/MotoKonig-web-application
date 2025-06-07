# app/infrastructure/repositories/sql_club_invitation_repo.py

from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.club_invitation import ClubInvitation
from app.domain.ports.repositories.club_invitation import (
    IClubInvitationRepository,
)
from app.domain.ports.specs.club_invitation import (
    ClubInvitationSpecificationPort,
)
from app.domain.value_objects.club_role import ClubRole
from app.infrastructure.models.club_invitation import (
    ClubInvitation as ClubInvitationModel,
)


class SqlClubInvitationRepository(IClubInvitationRepository):
    """SQLAlchemy реализация репозитория приглашений в мотоклубы"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, invitation: ClubInvitation) -> ClubInvitation:
        """Добавить новое приглашение"""
        db_invitation = ClubInvitationModel(
            club_id=invitation.club_id,
            inviter_id=invitation.inviter_id,
            invitee_id=invitation.invitee_id,
            invited_role=invitation.invited_role,
            status=invitation.status,
            message=invitation.message,
            expires_at=invitation.expires_at.isoformat(),
            responded_at=invitation.responded_at.isoformat() if invitation.responded_at else None,
        )

        self.session.add(db_invitation)
        await self.session.flush()
        await self.session.refresh(db_invitation)

        # Обновляем доменную сущность
        invitation.id = db_invitation.id
        invitation.created_at = db_invitation.created_at
        invitation.updated_at = db_invitation.updated_at

        return invitation

    async def get(self, spec: ClubInvitationSpecificationPort) -> ClubInvitation | None:
        """Получить приглашение по спецификации"""
        statement = spec.to_query(select(ClubInvitationModel))
        result = await self.session.execute(statement)
        db_invitation = result.scalar_one_or_none()

        if db_invitation:
            return self._to_domain_entity(db_invitation)
        return None

    async def get_list(self, spec: ClubInvitationSpecificationPort | None = None) -> list[ClubInvitation]:
        """Получить список приглашений по спецификации"""
        statement = select(ClubInvitationModel)

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        invitations = result.scalars().all()

        return [self._to_domain_entity(inv) for inv in invitations]

    async def update(self, invitation: ClubInvitation) -> ClubInvitation:
        """Обновить приглашение"""
        db_invitation = await self.session.get(ClubInvitationModel, invitation.id)

        if db_invitation:
            # Обновляем поля
            db_invitation.status = invitation.status
            db_invitation.message = invitation.message
            db_invitation.expires_at = invitation.expires_at.isoformat()
            db_invitation.responded_at = invitation.responded_at.isoformat() if invitation.responded_at else None

            await self.session.flush()
            await self.session.refresh(db_invitation)

            # Обновляем timestamp в доменной сущности
            invitation.updated_at = db_invitation.updated_at

        return invitation

    async def delete(self, invitation_id: UUID) -> bool:
        """Удалить приглашение"""
        db_invitation = await self.session.get(ClubInvitationModel, invitation_id)

        if db_invitation:
            await self.session.delete(db_invitation)
            await self.session.flush()
            return True

        return False

    async def get_pending_invitation(self, club_id: UUID, invitee_id: UUID) -> ClubInvitation | None:
        """Получить активное приглашение для пользователя в клуб"""
        statement = select(ClubInvitationModel).where(
            ClubInvitationModel.club_id == club_id,
            ClubInvitationModel.invitee_id == invitee_id,
            ClubInvitationModel.status == "pending"
        )
        result = await self.session.execute(statement)
        db_invitation = result.scalar_one_or_none()

        if db_invitation:
            invitation = self._to_domain_entity(db_invitation)
            # Проверяем, не истекло ли приглашение
            if invitation.is_expired():
                return None
            return invitation
        return None

    async def expire_old_invitations(self) -> int:
        """Сделать просроченными старые приглашения"""
        current_time = datetime.utcnow().isoformat()

        statement = (
            update(ClubInvitationModel)
            .where(
                ClubInvitationModel.status == "pending",
                ClubInvitationModel.expires_at < current_time
            )
            .values(
                status="expired",
                responded_at=current_time
            )
        )

        result = await self.session.execute(statement)
        await self.session.flush()

        return result.rowcount or 0

    def _to_domain_entity(self, db_invitation: ClubInvitationModel) -> ClubInvitation:
        """Преобразовать модель БД в доменную сущность"""
        expires_at = datetime.fromisoformat(db_invitation.expires_at)
        responded_at = None
        if db_invitation.responded_at:
            responded_at = datetime.fromisoformat(db_invitation.responded_at)

        return ClubInvitation(
            invitation_id=db_invitation.id,
            club_id=db_invitation.club_id,
            inviter_id=db_invitation.inviter_id,
            invitee_id=db_invitation.invitee_id,
            invited_role=ClubRole(db_invitation.invited_role.value),
            status=db_invitation.status,
            message=db_invitation.message,
            expires_at=expires_at,
            responded_at=responded_at,
            created_at=db_invitation.created_at,
            updated_at=db_invitation.updated_at
        )
