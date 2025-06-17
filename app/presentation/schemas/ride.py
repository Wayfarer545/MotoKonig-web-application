# app/presentation/schemas/ride.py

import datetime as dt
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from app.domain.value_objects.ride_difficulty import RideDifficulty


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


class CreateRideSchema(_BaseModel):
    """Схема для создания поездки"""
    title: str = Field(..., min_length=5, max_length=100, description="Название поездки")
    description: str | None = Field(None, max_length=2000, description="Описание")
    difficulty: RideDifficulty = Field(..., description="Сложность маршрута")
    planned_distance: int = Field(..., gt=0, le=5000, description="Планируемая дистанция в км")
    max_participants: int = Field(10, ge=2, le=50, description="Максимум участников")
    start_location: str = Field(..., min_length=3, max_length=200, description="Место старта")
    end_location: str | None = Field(None, max_length=200, description="Место финиша")
    planned_start: dt.datetime = Field(..., description="Планируемое время старта")
    planned_duration: int = Field(..., gt=0, le=1440, description="Планируемая продолжительность в минутах")
    route_gpx: str | None = Field(None, description="GPX маршрут")
    is_public: bool = Field(True, description="Публичная поездка")

    @field_validator('planned_start')
    @classmethod
    def validate_start_time(cls, v: dt.datetime) -> dt.datetime:
        if v <= dt.datetime.now(dt.UTC):
            raise ValueError("Start time must be in the future")
        return v


class JoinRideSchema(_BaseModel):
    """Схема для присоединения к поездке"""
    # MotoKonig ID берётся из токена авторизации
    pass


class CompleteRideSchema(_BaseModel):
    """Схема для завершения поездки"""
    actual_distance: int = Field(..., gt=0, description="Фактическая дистанция в км")
    weather_conditions: str | None = Field(None, max_length=200, description="Погодные условия")


class RateRideSchema(_BaseModel):
    """Схема для оценки поездки"""
    rating: float = Field(..., ge=0, le=5, description="Оценка от 0 до 5")


class RideParticipantSchema(BaseModel):
    """Схема участника поездки"""
    motokonig_id: UUID
    nickname: str
    avatar_url: str | None
    joined_at: dt.datetime
    is_leader: bool
    distance_covered: int | None
    average_speed: float | None
    max_speed: float | None


class RideResponseSchema(BaseModel):
    """Схема ответа для поездки"""
    ride_id: UUID
    organizer_id: UUID
    organizer_nickname: str | None = None
    title: str
    description: str | None
    difficulty: RideDifficulty
    planned_distance: int
    max_participants: int
    current_participants: int
    start_location: str
    end_location: str
    planned_start: dt.datetime
    planned_duration: int
    actual_start: dt.datetime | None
    actual_end: dt.datetime | None
    actual_distance: int | None
    weather_conditions: str | None
    is_public: bool
    is_completed: bool
    rating: float | None
    participants: list[RideParticipantSchema] | None = None
    created_at: dt.datetime
    updated_at: dt.datetime


class RideListItemSchema(BaseModel):
    """Схема элемента списка поездок"""
    ride_id: UUID
    title: str
    difficulty: RideDifficulty
    planned_distance: int
    start_location: str
    planned_start: dt.datetime
    current_participants: int
    max_participants: int
    is_completed: bool
    organizer_nickname: str | None = None
