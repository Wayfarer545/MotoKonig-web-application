# app/application/use_cases/moto_club/create_club.py

from uuid import UUID

from app.domain.entities.club_membership import ClubMembership
from app.domain.entities.moto_club import MotoClub
from app.domain.ports.repositories.club_membership import (
    IClubMembershipRepository,
)
from app.domain.ports.repositories.moto_club import IMotoClubRepository
from app.domain.value_objects.club_role import ClubRole


class CreateMotoClubUseCase:
    """Use case для создания мотоклуба"""

    def __init__(
            self,
            club_repo: IMotoClubRepository,
            membership_repo: IClubMembershipRepository
    ):
        self.club_repo = club_repo
        self.membership_repo = membership_repo

    async def execute(
            self,
            name: str,
            president_id: UUID,
            description: str | None = None,
            is_public: bool = True,
            max_members: int | None = None,
            location: str | None = None,
            website: str | None = None,
    ) -> MotoClub:
        """
        Создать новый мотоклуб

        Args:
            name: Название клуба
            president_id: ID создателя (будущего президента)
            description: Описание клуба
            is_public: Публичный ли клуб
            max_members: Максимальное количество участников
            location: Местоположение клуба
            website: Сайт клуба

        Returns:
            MotoClub: Созданный мотоклуб

        Raises:
            ValueError: При некорректных данных
        """
        # Создаем клуб
        club = MotoClub(
            name=name,
            description=description,
            president_id=president_id,
            is_public=is_public,
            max_members=max_members,
            location=location,
            website=website,
        )

        # Сохраняем клуб в БД
        saved_club = await self.club_repo.add(club)

        # Создаем членство для президента
        president_membership = ClubMembership(
            club_id=saved_club.id,
            user_id=president_id,
            role=ClubRole.PRESIDENT,
            status="active",
        )

        await self.membership_repo.add(president_membership)

        return saved_club
