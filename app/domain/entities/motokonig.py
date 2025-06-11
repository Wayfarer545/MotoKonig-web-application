# app/domain/entities/motokonig.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.entities.achievement import Achievement
from app.domain.value_objects.motokonig_status import MotoKonigStatus
from app.domain.value_objects.achievement_type import AchievementType

__all__ = ["MotoKonig"]

if TYPE_CHECKING:
    pass
    """Достижение MotoKonig"""

    def __init__(
            self,
            *,
            achievement_id: UUID | None = None,
            achievement_type: AchievementType,
            earned_at: datetime | None = None,
            description: str | None = None,
            metadata: dict | None = None
    ):
        self.achievement_id = achievement_id or uuid4()
        self.achievement_type = achievement_type
        self.earned_at = earned_at or datetime.utcnow()
        self.description = description
        self.metadata = metadata or {}




class MotoKonig:
    """
    Доменная сущность MotoKonig - профиль мотоциклиста

    Инварианты:
    - Уровень опыта не может быть отрицательным
    - Общий пробег не может быть отрицательным
    - Количество поездок не может быть отрицательным
    - Рейтинг должен быть от 0 до 5
    - Статус должен соответствовать уровню опыта
    """

    def __init__(
            self,
            *,
            motokonig_id: UUID | None = None,
            user_id: UUID,
            nickname: str,
            status: MotoKonigStatus = MotoKonigStatus.NOVICE,
            experience_points: int = 0,
            total_distance: int = 0,  # в километрах
            total_rides: int = 0,
            average_speed: float | None = None,
            max_speed: float | None = None,
            favorite_routes: list[UUID] | None = None,
            achievements: list[Achievement] | None = None,
            rating: float = 0.0,
            bio: str | None = None,
            avatar_url: str | None = None,
            is_public: bool = True,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Валидация
        if experience_points < 0:
            raise ValueError("Experience points cannot be negative")
        if total_distance < 0:
            raise ValueError("Total distance cannot be negative")
        if total_rides < 0:
            raise ValueError("Total rides cannot be negative")
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        if len(nickname) < 3 or len(nickname) > 30:
            raise ValueError("Nickname must be between 3 and 30 characters")

        self.motokonig_id = motokonig_id or uuid4()
        self.user_id = user_id
        self.nickname = nickname.strip()
        self.status = status
        self.experience_points = experience_points
        self.total_distance = total_distance
        self.total_rides = total_rides
        self.average_speed = average_speed
        self.max_speed = max_speed
        self.favorite_routes = favorite_routes or []
        self.achievements = achievements or []
        self.rating = rating
        self.bio = bio.strip() if bio else None
        self.avatar_url = avatar_url
        self.is_public = is_public
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def add_achievement(self, achievement: Achievement) -> None:
        """Добавить достижение"""
        if any(a.achievement_type == achievement.achievement_type for a in self.achievements):
            raise ValueError(f"Achievement {achievement.achievement_type} already earned")

        self.achievements.append(achievement)
        self._add_experience_for_achievement(achievement.achievement_type)
        self.updated_at = datetime.utcnow()

    def _add_experience_for_achievement(self, achievement_type: AchievementType) -> None:
        """Начислить опыт за достижение"""
        points_map = {
            AchievementType.FIRST_RIDE: 100,
            AchievementType.DISTANCE_100K: 500,
            AchievementType.DISTANCE_1000K: 2000,
            AchievementType.SPEED_DEMON: 300,
            AchievementType.NIGHT_RIDER: 400,
            AchievementType.RAIN_MASTER: 600,
            AchievementType.TRACK_DAY: 1000,
            AchievementType.CUSTOM_BUILD: 1500,
            AchievementType.GROUP_RIDE: 200,
            AchievementType.MENTOR: 800,
        }

        self.experience_points += points_map.get(achievement_type, 100)
        self._update_status()

    def _update_status(self) -> None:
        """Обновить статус на основе опыта"""
        if self.experience_points >= 10000:
            self.status = MotoKonigStatus.KONIG
        elif self.experience_points >= 5000:
            self.status = MotoKonigStatus.LEGEND
        elif self.experience_points >= 2500:
            self.status = MotoKonigStatus.MASTER
        elif self.experience_points >= 1000:
            self.status = MotoKonigStatus.EXPERT
        elif self.experience_points >= 500:
            self.status = MotoKonigStatus.RIDER
        else:
            self.status = MotoKonigStatus.NOVICE

    def update_ride_stats(self, distance: int, duration: int, max_speed: float) -> None:
        """Обновить статистику после поездки"""
        if distance < 0 or duration <= 0:
            raise ValueError("Invalid ride parameters")

        self.total_distance += distance
        self.total_rides += 1

        # Обновляем максимальную скорость
        if self.max_speed is None or max_speed > self.max_speed:
            self.max_speed = max_speed

        # Пересчитываем среднюю скорость
        ride_avg_speed = (distance / duration) * 60  # км/ч
        if self.average_speed is None:
            self.average_speed = ride_avg_speed
        else:
            # Взвешенное среднее
            self.average_speed = (
                    (self.average_speed * (self.total_rides - 1) + ride_avg_speed)
                    / self.total_rides
            )

        # Начисляем опыт за поездку
        self.experience_points += self._calculate_ride_experience(distance, max_speed)
        self._update_status()
        self.updated_at = datetime.utcnow()

    def _calculate_ride_experience(self, distance: int, max_speed: float) -> int:
        """Рассчитать опыт за поездку"""
        base_points = distance // 10  # 1 очко за каждые 10 км

        # Бонусы за скорость (но не поощряем превышение)
        if 80 <= max_speed <= 120:
            speed_bonus = 10
        elif 120 < max_speed <= 150:
            speed_bonus = 20
        else:
            speed_bonus = 0

        return base_points + speed_bonus

    def to_dto(self) -> dict:
        """Преобразовать в DTO"""
        return {
            "motokonig_id": self.motokonig_id,
            "user_id": self.user_id,
            "nickname": self.nickname,
            "status": self.status,
            "experience_points": self.experience_points,
            "total_distance": self.total_distance,
            "total_rides": self.total_rides,
            "average_speed": self.average_speed,
            "max_speed": self.max_speed,
            "favorite_routes": self.favorite_routes,
            "achievements": [
                {
                    "achievement_id": a.achievement_id,
                    "achievement_type": a.achievement_type,
                    "earned_at": a.earned_at,
                    "description": a.description,
                    "metadata": a.metadata
                }
                for a in self.achievements
            ],
            "rating": self.rating,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "is_public": self.is_public,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }