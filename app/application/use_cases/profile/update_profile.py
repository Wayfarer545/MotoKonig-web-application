# app/application/use_cases/profile/update_profile.py

from datetime import date
from uuid import UUID

from app.domain.entities.profile import PrivacyLevel, Profile
from app.domain.ports.epositories.profile_repository import IProfileRepository
from app.infrastructure.specs.profile.profile_by_id import ProfileById


class UpdateProfileUseCase:
    """Use case для обновления профиля"""

    def __init__(self, repo: IProfileRepository):
        self.repo = repo

    async def execute(
            self,
            profile_id: UUID,
            bio: str | None = None,
            location: str | None = None,
            phone: str | None = None,
            date_of_birth: date | None = None,
            riding_experience: int | None = None,
            avatar_url: str | None = None,
            privacy_level: PrivacyLevel | None = None,
            phone_privacy: PrivacyLevel | None = None,
            location_privacy: PrivacyLevel | None = None,
    ) -> Profile | None:
        """Обновить данные профиля"""
        existing = await self.repo.get(ProfileById(profile_id))

        if not existing:
            return None

        # Обновляем только переданные поля
        if bio is not None:
            existing.update_bio(bio)
        if location is not None:
            existing.update_location(location)
        if phone is not None:
            existing.update_phone(phone)
        if date_of_birth is not None:
            existing._validate_date_of_birth(date_of_birth)
            existing.date_of_birth = date_of_birth
        if riding_experience is not None:
            existing._validate_riding_experience(riding_experience)
            existing.riding_experience = riding_experience
        if avatar_url is not None:
            existing.update_avatar(avatar_url)
        if privacy_level is not None:
            existing.set_privacy_level(privacy_level)
        if phone_privacy is not None:
            existing.set_phone_privacy(phone_privacy)
        if location_privacy is not None:
            existing.set_location_privacy(location_privacy)

        return await self.repo.update(existing)
