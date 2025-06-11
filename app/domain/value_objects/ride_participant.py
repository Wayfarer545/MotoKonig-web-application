# app/domain/value_objects/ride_participant.py

from datetime import datetime
from uuid import UUID

__all__ = ["RideParticipant"]


class RideParticipant:
    """
    Value Object участника поездки

    Инварианты:
    - Расстояние не может быть отрицательным
    - Средняя и максимальная скорость должны быть положительными
    - Время выхода не может быть раньше времени входа
    """

    def __init__(
            self,
            *,
            motokonig_id: UUID,
            joined_at: datetime | None = None,
            left_at: datetime | None = None,
            distance_covered: int = 0,
            average_speed: float | None = None,
            max_speed: float | None = None,
            is_leader: bool = False
    ):
        # Валидация
        if distance_covered < 0:
            raise ValueError("Distance covered cannot be negative")

        if average_speed is not None and average_speed <= 0:
            raise ValueError("Average speed must be positive")

        if max_speed is not None and max_speed <= 0:
            raise ValueError("Max speed must be positive")

        if joined_at and left_at and left_at < joined_at:
            raise ValueError("Cannot leave before joining")

        self.motokonig_id = motokonig_id
        self.joined_at = joined_at or datetime.utcnow()
        self.left_at = left_at
        self.distance_covered = distance_covered
        self.average_speed = average_speed
        self.max_speed = max_speed
        self.is_leader = is_leader

    def __eq__(self, other):
        if not isinstance(other, RideParticipant):
            return NotImplemented
        return self.motokonig_id == other.motokonig_id
