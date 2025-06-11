# app/application/use_cases/motokonig/update_ride_stats.py

from uuid import UUID

from app.domain.entities.motokonig import MotoKonig
from app.domain.ports.repositories.motokonig import IMotoKonigRepository

__all__ = ["UpdateRideStatsUseCase"]


class UpdateRideStatsUseCase:
    """Use case для обновления статистики после поездки"""

    def __init__(self, motokonig_repo: IMotoKonigRepository):
        self._motokonig_repo = motokonig_repo

    async def execute(
            self,
            motokonig_id: UUID,
            distance: int,
            duration: int,  # в минутах
            max_speed: float,
    ) -> MotoKonig:
        """Обновить статистику профиля после поездки"""

        # Получаем профиль
        motokonig = await self._motokonig_repo.get_by_id(motokonig_id)
        if not motokonig:
            raise ValueError("MotoKonig profile not found")

        # Обновляем статистику
        motokonig.update_ride_stats(distance, duration, max_speed)

        # Проверяем достижения
        await self._check_achievements(motokonig, distance, max_speed)

        # Сохраняем
        return await self._motokonig_repo.update(motokonig)

    async def _check_achievements(
            self,
            motokonig: MotoKonig,
            distance: int,
            max_speed: float
    ) -> None:
        """Проверить и начислить достижения"""
        from app.domain.entities.achievement import Achievement
        from app.domain.value_objects.achievement_type import AchievementType

        # Первая поездка
        if motokonig.total_rides == 1:
            achievement = Achievement(
                achievement_type=AchievementType.FIRST_RIDE,
                description="Совершил свою первую поездку!"
            )
            motokonig.add_achievement(achievement)

        # 100к км
        if motokonig.total_distance >= 100 and motokonig.total_distance - distance < 100:
            achievement = Achievement(
                achievement_type=AchievementType.DISTANCE_100K,
                description="Проехал 100 километров!"
            )
            motokonig.add_achievement(achievement)

        # Скоростной демон
        if max_speed >= 200:
            has_achievement = any(
                a.achievement_type == AchievementType.SPEED_DEMON
                for a in motokonig.achievements
            )
            if not has_achievement:
                achievement = Achievement(
                    achievement_type=AchievementType.SPEED_DEMON,
                    description="Разогнался до 200+ км/ч!",
                    metadata={"max_speed": max_speed}
                )
                motokonig.add_achievement(achievement)
