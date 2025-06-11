# app/application/controllers/motokonig_controller.py

from uuid import UUID

from app.application.use_cases.motokonig.create_profile import (
    CreateMotoKonigProfileUseCase,
)
from app.application.use_cases.motokonig.get_top_riders import GetTopRidersUseCase
from app.application.use_cases.motokonig.update_ride_stats import UpdateRideStatsUseCase
from app.domain.entities.motokonig import MotoKonig
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.infrastructure.specs.motokonig.motokonig_by_id import MotoKonigById
from app.infrastructure.specs.motokonig.motokonig_by_user_id import MotoKonigByUserId

__all__ = ["MotoKonigController"]


class MotoKonigController:
    """Контроллер для управления профилями MotoKonig"""

    def __init__(
            self,
            motokonig_repo: IMotoKonigRepository,
            create_profile_uc: CreateMotoKonigProfileUseCase,
            update_stats_uc: UpdateRideStatsUseCase,
            get_top_riders_uc: GetTopRidersUseCase,
    ):
        self._motokonig_repo = motokonig_repo
        self._create_profile_uc = create_profile_uc
        self._update_stats_uc = update_stats_uc
        self._get_top_riders_uc = get_top_riders_uc

    async def create_profile(
            self,
            user_id: UUID,
            nickname: str,
            bio: str | None = None,
            avatar_url: str | None = None,
            is_public: bool = True,
    ) -> MotoKonig:
        """Создать профиль MotoKonig"""
        return await self._create_profile_uc.execute(
            user_id=user_id,
            nickname=nickname,
            bio=bio,
            avatar_url=avatar_url,
            is_public=is_public,
        )

    async def get_profile_by_id(self, motokonig_id: UUID) -> MotoKonig | None:
        """Получить профиль по ID"""
        return await self._motokonig_repo.get(MotoKonigById(motokonig_id))

    async def get_profile_by_user_id(self, user_id: UUID) -> MotoKonig | None:
        """Получить профиль по ID пользователя"""
        return await self._motokonig_repo.get(MotoKonigByUserId(user_id))

    async def update_profile(
            self,
            motokonig_id: UUID,
            nickname: str | None = None,
            bio: str | None = None,
            avatar_url: str | None = None,
            is_public: bool | None = None,
    ) -> MotoKonig:
        """Обновить профиль"""
        profile = await self.get_profile_by_id(motokonig_id)
        if not profile:
            raise ValueError("MotoKonig profile not found")

        # Обновляем только переданные поля
        if nickname is not None:
            profile.nickname = nickname
        if bio is not None:
            profile.bio = bio
        if avatar_url is not None:
            profile.avatar_url = avatar_url
        if is_public is not None:
            profile.is_public = is_public

        return await self._motokonig_repo.update(profile)

    async def delete_profile(self, motokonig_id: UUID) -> None:
        """Удалить профиль"""
        await self._motokonig_repo.delete(motokonig_id)

    async def get_top_riders(self, limit: int = 10) -> list[MotoKonig]:
        """Получить топ райдеров"""
        return await self._get_top_riders_uc.execute(limit)

    async def update_ride_statistics(
            self,
            motokonig_id: UUID,
            distance: int,
            duration: int,
            max_speed: float,
    ) -> MotoKonig:
        """Обновить статистику после поездки"""
        return await self._update_stats_uc.execute(
            motokonig_id=motokonig_id,
            distance=distance,
            duration=duration,
            max_speed=max_speed,
        )
