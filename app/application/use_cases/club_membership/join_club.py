# app/application/use_cases/club_membership/join_club.py

from uuid import UUID

from app.domain.entities.club_membership import ClubMembership
from app.domain.ports.club_membership_repository import IClubMembershipRepository
from app.domain.ports.moto_club_repository import IMotoClubRepository
from app.domain.value_objects.club_role import ClubRole
from app.infrastructure.specs.moto_club.club_by_id import MotoClubById


class JoinClubUseCase:
    """Use case для вступления в мотоклуб"""

    def __init__(
            self,
            club_repo: IMotoClubRepository,
            membership_repo: IClubMembershipRepository
    ):
        self.club_repo = club_repo
        self.membership_repo = membership_repo

    async def execute(
            self,
            club_id: UUID,
            user_id: UUID,
            role: ClubRole = ClubRole.MEMBER
    ) -> ClubMembership:
        """
        Вступить в мотоклуб

        Args:
            club_id: ID клуба
            user_id: ID пользователя
            role: Роль в клубе (по умолчанию MEMBER)

        Returns:
            ClubMembership: Созданное членство

        Raises:
            ValueError: При некорректных условиях вступления
        """
        # Проверяем, что клуб существует и активен
        club = await self.club_repo.get(MotoClubById(club_id))
        if not club:
            raise ValueError("Club not found")

        if not club.is_active:
            raise ValueError("Club is not active")

        # Проверяем, что пользователь еще не является участником
        existing_membership = await self.membership_repo.get_user_membership_in_club(
            user_id, club_id
        )
        if existing_membership:
            raise ValueError("User is already a member of this club")

        # Проверяем лимит участников
        if club.max_members:
            current_count = await self.membership_repo.count_club_members(club_id)
            if current_count >= club.max_members:
                raise ValueError("Club has reached maximum member limit")

        # Создаем членство
        membership = ClubMembership(
            club_id=club_id,
            user_id=user_id,
            role=role,
            status="active",
        )

        return await self.membership_repo.add(membership)
