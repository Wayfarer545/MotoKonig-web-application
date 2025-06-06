# app/application/controllers/profile_controller.py

from datetime import date
from uuid import UUID

from app.application.exceptions import NotFoundError
from app.application.use_cases.profile.create_profile import CreateProfileUseCase
from app.application.use_cases.profile.delete_profile import DeleteProfileUseCase
from app.application.use_cases.profile.get_profile import GetProfileUseCase
from app.application.use_cases.profile.update_profile import UpdateProfileUseCase
from app.application.use_cases.social_link.add_social_link import AddSocialLinkUseCase
from app.application.use_cases.social_link.get_profile_social_links import (
    GetProfileSocialLinksUseCase,
)
from app.application.use_cases.social_link.remove_social_link import (
    RemoveSocialLinkUseCase,
)
from app.domain.entities.profile import PrivacyLevel, Profile
from app.domain.entities.social_link import SocialPlatform
from app.infrastructure.specs.profile.profile_by_id import ProfileById
from app.infrastructure.specs.profile.profile_by_user_id import ProfileByUserId


class ProfileController:
    """Контроллер для управления профилями"""

    def __init__(
            self,
            create_profile_uc: CreateProfileUseCase,
            get_profile_uc: GetProfileUseCase,
            update_profile_uc: UpdateProfileUseCase,
            delete_profile_uc: DeleteProfileUseCase,
            add_social_link_uc: AddSocialLinkUseCase,
            remove_social_link_uc: RemoveSocialLinkUseCase,
            get_social_links_uc: GetProfileSocialLinksUseCase,
    ):
        self.create_profile_uc = create_profile_uc
        self.get_profile_uc = get_profile_uc
        self.update_profile_uc = update_profile_uc
        self.delete_profile_uc = delete_profile_uc
        self.add_social_link_uc = add_social_link_uc
        self.remove_social_link_uc = remove_social_link_uc
        self.get_social_links_uc = get_social_links_uc

    async def create_profile(
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
        return await self.create_profile_uc.execute(
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

    async def get_profile_by_id(
            self,
            profile_id: UUID,
            viewer_role: str = "USER",
            is_friend: bool = False,
            is_club_member: bool = False
    ) -> dict:
        """Получить профиль по ID"""
        spec = ProfileById(profile_id)
        profile = await self.get_profile_uc.execute(spec)

        if not profile:
            raise NotFoundError("Profile not found")

        return profile.to_dto(viewer_role, is_friend, is_club_member)

    async def get_profile_by_user_id(
            self,
            user_id: UUID,
            viewer_role: str = "USER",
            is_friend: bool = False,
            is_club_member: bool = False
    ) -> dict:
        """Получить профиль по ID пользователя"""
        spec = ProfileByUserId(user_id)
        profile = await self.get_profile_uc.execute(spec)

        if not profile:
            raise NotFoundError("Profile not found")

        return profile.to_dto(viewer_role, is_friend, is_club_member)

    async def update_profile(
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
            viewer_role: str = "USER",
            is_friend: bool = False,
            is_club_member: bool = False
    ) -> dict:
        """Обновить профиль"""
        updated = await self.update_profile_uc.execute(
            profile_id=profile_id,
            bio=bio,
            location=location,
            phone=phone,
            date_of_birth=date_of_birth,
            riding_experience=riding_experience,
            avatar_url=avatar_url,
            privacy_level=privacy_level,
            phone_privacy=phone_privacy,
            location_privacy=location_privacy,
        )

        if not updated:
            raise NotFoundError("Profile not found")

        return updated.to_dto(viewer_role, is_friend, is_club_member)

    async def delete_profile(self, profile_id: UUID) -> None:
        """Удалить профиль"""
        success = await self.delete_profile_uc.execute(profile_id)
        if not success:
            raise NotFoundError("Profile not found")

    async def add_social_link(
            self,
            profile_id: UUID,
            platform: SocialPlatform,
            url: str,
            privacy_level: PrivacyLevel = PrivacyLevel.FRIENDS_ONLY,
            viewer_role: str = "USER",
            is_friend: bool = False,
            is_club_member: bool = False
    ) -> dict:
        """Добавить социальную ссылку"""
        social_link = await self.add_social_link_uc.execute(
            profile_id=profile_id,
            platform=platform,
            url=url,
            privacy_level=privacy_level,
        )
        return social_link.to_dto(viewer_role, is_friend, is_club_member)

    async def remove_social_link(
            self,
            profile_id: UUID,
            platform: SocialPlatform
    ) -> None:
        """Удалить социальную ссылку"""
        success = await self.remove_social_link_uc.execute(profile_id, platform)
        if not success:
            raise NotFoundError("Social link not found")

    async def get_profile_social_links(
            self,
            profile_id: UUID,
            viewer_role: str = "USER",
            is_friend: bool = False,
            is_club_member: bool = False
    ) -> list[dict]:
        """Получить социальные ссылки профиля"""
        social_links = await self.get_social_links_uc.execute(profile_id)
        return [link.to_dto(viewer_role, is_friend, is_club_member) for link in social_links]
