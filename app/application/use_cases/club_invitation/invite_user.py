# app/application/use_cases/club_invitation/invite_user.py

from uuid import UUID

from app.domain.entities.club_invitation import ClubInvitation
from app.domain.ports.epositories.club_invitation_repository import (
    IClubInvitationRepository,
)
from app.domain.ports.epositories.club_membership_repository import (
    IClubMembershipRepository,
)
from app.domain.ports.epositories.moto_club_repository import IMotoClubRepository
from app.domain.value_objects.club_role import ClubRole
from app.infrastructure.specs.moto_club.club_by_id import MotoClubById


class InviteUserToClubUseCase:
    """Use case для приглашения пользователя в мотоклуб"""

    def __init__(
            self,
            club_repo: IMotoClubRepository,
            membership_repo: IClubMembershipRepository,
            invitation_repo: IClubInvitationRepository
    ):
        self.club_repo = club_repo
        self.membership_repo = membership_repo
        self.invitation_repo = invitation_repo

    async def execute(
            self,
            club_id: UUID,
            inviter_id: UUID,
            invitee_id: UUID,
            invited_role: ClubRole = ClubRole.MEMBER,
            message: str | None = None
    ) -> ClubInvitation:
        """
        Пригласить пользователя в мотоклуб

        Args:
            club_id: ID клуба
            inviter_id: ID приглашающего
            invitee_id: ID приглашаемого
            invited_role: Предлагаемая роль
            message: Персональное сообщение

        Returns:
            ClubInvitation: Созданное приглашение

        Raises:
            ValueError: При некорректных условиях приглашения
        """
        # Проверяем, что клуб существует и активен
        club = await self.club_repo.get(MotoClubById(club_id))
        if not club:
            raise ValueError("Club not found")

        if not club.is_active:
            raise ValueError("Club is not active")

        # Проверяем права приглашающего
        inviter_membership = await self.membership_repo.get_user_membership_in_club(
            inviter_id, club_id
        )
        if not inviter_membership or not inviter_membership.is_active():
            raise ValueError("Inviter is not an active member of this club")

        if not inviter_membership.role.can_invite_members():
            raise ValueError("Inviter doesn't have permission to invite members")

        # Проверяем, что приглашаемый еще не является участником
        existing_membership = await self.membership_repo.get_user_membership_in_club(
            invitee_id, club_id
        )
        if existing_membership:
            raise ValueError("User is already a member of this club")

        # Проверяем, что нет активного приглашения
        existing_invitation = await self.invitation_repo.get_pending_invitation(
            club_id, invitee_id
        )
        if existing_invitation:
            raise ValueError("User already has a pending invitation to this club")

        # Проверяем лимит участников
        if club.max_members:
            current_count = await self.membership_repo.count_club_members(club_id)
            if current_count >= club.max_members:
                raise ValueError("Club has reached maximum member limit")

        # Создаем приглашение
        invitation = ClubInvitation(
            club_id=club_id,
            inviter_id=inviter_id,
            invitee_id=invitee_id,
            invited_role=invited_role,
            message=message,
        )

        return await self.invitation_repo.add(invitation)



