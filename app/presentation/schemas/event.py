# app/presentation/schemas/event.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from app.domain.value_objects.event_type import EventType
from app.domain.value_objects.location import Location


class BaseModel(_BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LocationSchema(_BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: str | None = Field(None, max_length=200)

    def to_vo(self) -> Location:
        return Location(latitude=self.latitude, longitude=self.longitude, address=self.address)


class CreateEventSchema(_BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    location: LocationSchema
    start_time: datetime
    end_time: datetime | None = None
    event_type: EventType = Field(EventType.PRIVATE)
    max_participants: int | None = Field(None, ge=1, le=10000)
    photo_urls: list[str] | None = Field(None, max_items=10)

    @field_validator("title", "description")
    @classmethod
    def strip(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class UpdateEventSchema(_BaseModel):
    title: str | None = Field(None, min_length=3, max_length=200)
    description: str | None = Field(None, min_length=10, max_length=5000)
    location: LocationSchema | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    event_type: EventType | None = None
    max_participants: int | None = Field(None, ge=1, le=10000)
    photo_urls: list[str] | None = Field(None, max_items=10)


class EventResponseSchema(BaseModel):
    id: UUID
    organizer_id: UUID
    title: str
    description: str
    location: dict
    start_time: datetime
    end_time: datetime | None
    event_type: str
    max_participants: int | None
    photo_urls: list[str]
    created_at: datetime
    updated_at: datetime
