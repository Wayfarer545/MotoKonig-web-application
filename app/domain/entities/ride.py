# app/domain/entities/ride.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.ride_checkpoint import RideCheckpoint
from app.domain.value_objects.ride_difficulty import RideDifficulty
from app.domain.value_objects.ride_participant import RideParticipant

__all__ = ["Ride"]

if TYPE_CHECKING:
    pass


class Ride:
    """
    Доменная сущность поездки

    Инварианты:
    - Дата начала не может быть позже даты окончания
    - Расстояние не может быть отрицательным
    - Максимальное количество участников должно быть положительным
    - Продолжительность должна быть положительной
    """

    def __init__(
            self,
            *,
            ride_id: UUID | None = None,
            organizer_id: UUID,
            title: str,
            description: str | None = None,
            difficulty: RideDifficulty,
            planned_distance: int,  # в километрах
            max_participants: int = 10,
            start_location: str,
            end_location: str | None = None,
            planned_start: datetime,
            planned_duration: int,  # в минутах
            actual_start: datetime | None = None,
            actual_end: datetime | None = None,
            actual_distance: int | None = None,
            route_gpx: str | None = None,  # GPX файл маршрута
            weather_conditions: str | None = None,
            participants: list[RideParticipant] | None = None,
            checkpoints: list[RideCheckpoint] | None = None,
            is_public: bool = True,
            is_completed: bool = False,
            rating: float | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Валидация
        if planned_distance <= 0:
            raise ValueError("Planned distance must be positive")
        if max_participants <= 0:
            raise ValueError("Max participants must be positive")
        if planned_duration <= 0:
            raise ValueError("Planned duration must be positive")
        if len(title) < 5 or len(title) > 100:
            raise ValueError("Title must be between 5 and 100 characters")
        if actual_start and actual_end and actual_start > actual_end:
            raise ValueError("Start time cannot be after end time")

        self.ride_id = ride_id or uuid4()
        self.organizer_id = organizer_id
        self.title = title.strip()
        self.description = description.strip() if description else None
        self.difficulty = difficulty
        self.planned_distance = planned_distance
        self.max_participants = max_participants
        self.start_location = start_location.strip()
        self.end_location = end_location.strip() if end_location else start_location
        self.planned_start = planned_start
        self.planned_duration = planned_duration
        self.actual_start = actual_start
        self.actual_end = actual_end
        self.actual_distance = actual_distance
        self.route_gpx = route_gpx
        self.weather_conditions = weather_conditions
        self.participants = participants or []
        self.checkpoints = checkpoints or []
        self.is_public = is_public
        self.is_completed = is_completed
        self.rating = rating
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def add_participant(self, motokonig_id: UUID, is_leader: bool = False) -> None:
        """Добавить участника к поездке"""
        if any(p.motokonig_id == motokonig_id for p in self.participants):
            raise ValueError("Participant already in ride")

        if len(self.participants) >= self.max_participants:
            raise ValueError("Ride is full")

        if self.is_completed:
            raise ValueError("Cannot join completed ride")

        participant = RideParticipant(
            motokonig_id=motokonig_id,
            is_leader=is_leader
        )
        self.participants.append(participant)
        self.updated_at = datetime.utcnow()

    def remove_participant(self, motokonig_id: UUID) -> None:
        """Удалить участника из поездки"""
        participant = next((p for p in self.participants if p.motokonig_id == motokonig_id), None)
        if not participant:
            raise ValueError("Participant not found in ride")

        if self.is_completed:
            raise ValueError("Cannot leave completed ride")

        participant.left_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def start_ride(self) -> None:
        """Начать поездку"""
        if self.is_completed:
            raise ValueError("Ride already completed")
        if self.actual_start:
            raise ValueError("Ride already started")

        self.actual_start = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def complete_ride(self, actual_distance: int, weather_conditions: str | None = None) -> None:
        """Завершить поездку"""
        if not self.actual_start:
            raise ValueError("Cannot complete ride that hasn't started")
        if self.is_completed:
            raise ValueError("Ride already completed")
        if actual_distance <= 0:
            raise ValueError("Actual distance must be positive")

        self.actual_end = datetime.utcnow()
        self.actual_distance = actual_distance
        self.weather_conditions = weather_conditions
        self.is_completed = True
        self.updated_at = datetime.utcnow()

    def add_checkpoint(self, checkpoint: RideCheckpoint) -> None:
        """Добавить контрольную точку"""
        if self.is_completed:
            raise ValueError("Cannot add checkpoint to completed ride")

        self.checkpoints.append(checkpoint)
        self.updated_at = datetime.utcnow()

    def rate_ride(self, rating: float) -> None:
        """Оценить поездку"""
        if not self.is_completed:
            raise ValueError("Cannot rate incomplete ride")
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")

        self.rating = rating
        self.updated_at = datetime.utcnow()

    def to_dto(self) -> dict:
        """Преобразовать в DTO"""
        return {
            "ride_id": self.ride_id,
            "organizer_id": self.organizer_id,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty,
            "planned_distance": self.planned_distance,
            "max_participants": self.max_participants,
            "start_location": self.start_location,
            "end_location": self.end_location,
            "planned_start": self.planned_start,
            "planned_duration": self.planned_duration,
            "actual_start": self.actual_start,
            "actual_end": self.actual_end,
            "actual_distance": self.actual_distance,
            "route_gpx": self.route_gpx,
            "weather_conditions": self.weather_conditions,
            "participants": [
                {
                    "motokonig_id": p.motokonig_id,
                    "joined_at": p.joined_at,
                    "left_at": p.left_at,
                    "distance_covered": p.distance_covered,
                    "average_speed": p.average_speed,
                    "max_speed": p.max_speed,
                    "is_leader": p.is_leader
                }
                for p in self.participants
            ],
            "checkpoints": [
                {
                    "latitude": c.latitude,
                    "longitude": c.longitude,
                    "name": c.name,
                    "reached_at": c.reached_at
                }
                for c in self.checkpoints
            ],
            "is_public": self.is_public,
            "is_completed": self.is_completed,
            "rating": self.rating,
            "participants_count": len(self.participants),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
