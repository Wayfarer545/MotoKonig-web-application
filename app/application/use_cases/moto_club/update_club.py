# app/application/use_cases/moto_club/update_club.py

from uuid import UUID

from app.domain.entities.moto_club import MotoClub
from app.domain.ports.moto_club_repository import IMotoClubRepository
from app.infrastructure.specs.moto_club.club_by_id import MotoClubById


class UpdateMotoClubUseCase:
    """Use case для обновления мотоклуба"""

    def __init__(self, repo: IMotoClubRepository):
        self.repo = repo

    async def execute(
            self,
            club_id: UUID,
            name: str | None = None,
            description: str | None = None,
            is_public: bool | None = None,
            max_members: int | None = None,
            location: str | None = None,
            website: str | None = None,
            avatar_url: str | None = None,
    ) -> MotoClub | None:
        """Обновить данные мотоклуба"""
        existing = await self.repo.get(MotoClubById(club_id))

        if not existing:
            return None

        # Обновляем только переданные поля
        if name is not None:
            existing.update_name(name)
        if description is not None:
            existing.update_description(description)
        if location is not None:
            existing.update_location(location)
        if website is not None:
            existing.website = website.strip() if website else None
        if max_members is not None:
            existing.set_max_members(max_members)
        if is_public is not None:
            if is_public:
                existing.make_public()
            else:
                existing.make_private()
        if avatar_url is not None:
            existing.update_avatar(avatar_url)

        return await self.repo.update(existing)
