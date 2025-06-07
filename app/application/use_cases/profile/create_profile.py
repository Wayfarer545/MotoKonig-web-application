# app/application/use_cases/profile/create_profile.py

from datetime import date
from uuid import UUID

from app.domain.entities.profile import PrivacyLevel, Profile
from app.domain.ports.epositories.profile_repository import IProfileRepository


class CreateProfileUseCase:
    """Use case для создания профиля пользователя"""

    def __init__(self, repo: IProfileRepository):
        self.repo = repo

    async def execute(
            self,
            user_id: UUID,
            bio: str | None = None,
            location: str | None = None,
            phone: str | None = None,
            date_of_birth: date | None = None,
            riding_experience: int | None = None,
            privacy_level: PrivacyLevel = PrivacyLevel.PUBLIC,
            phone_privacy: PrivacyLevel = PrivacyLevel.FRIENDS_ONLY,
            location_privacy: PrivacyLevel = PrivacyLevel.PUBLIC,
    ) -> Profile:
        """Создать новый профиль"""
        profile = Profile(
            user_id=user_id,
            bio=bio,
            location=location,
            phone=phone,
            date_of_birth=date_of_birth,
            riding_experience=riding_experience,
            privacy_level=privacy_level,
            phone_privacy=phone_privacy,
            location_privacy=location_privacy,
        )

        return await self.repo.add(profile)
