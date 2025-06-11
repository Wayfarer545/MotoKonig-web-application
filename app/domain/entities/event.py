# app/domain/entities/event.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.event_type import EventType
from app.domain.value_objects.location import Location

if TYPE_CHECKING:
    pass


class Event:
    """Доменная сущность мероприятия"""

    def __init__(
            self,
            *,
            event_id: UUID | None = None,
            organizer_id: UUID,
            title: str,
            description: str,
            location: Location,
            start_time: datetime,
            end_time: datetime | None = None,
            event_type: EventType = EventType.PRIVATE,
            max_participants: int | None = None,
            photo_urls: list[str] | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ) -> None:
        self._validate_title(title)
        self._validate_description(description)
        if max_participants is not None:
            self._validate_max_participants(max_participants)
        if end_time is not None:
            self._validate_time_range(start_time, end_time)
        if photo_urls:
            self._validate_photo_urls(photo_urls)

        self.id: UUID = event_id or uuid4()
        self.organizer_id: UUID = organizer_id
        self.title: str = title.strip()
        self.description: str = description.strip()
        self.location: Location = location
        self.start_time: datetime = start_time
        self.end_time: datetime | None = end_time
        self.event_type: EventType = event_type
        self.max_participants: int | None = max_participants
        self.photo_urls: list[str] = photo_urls or []
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_title(self, title: str) -> None:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title.strip()) < 3:
            raise ValueError("Title must be at least 3 characters long")
        if len(title.strip()) > 200:
            raise ValueError("Title cannot be longer than 200 characters")

    def _validate_description(self, description: str) -> None:
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        if len(description.strip()) < 10:
            raise ValueError("Description must be at least 10 characters long")
        if len(description.strip()) > 5000:
            raise ValueError("Description cannot be longer than 5000 characters")

    def _validate_max_participants(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Max participants must be positive")
        if value > 10000:
            raise ValueError("Max participants cannot exceed 10000")

    def _validate_photo_urls(self, photo_urls: list[str]) -> None:
        if len(photo_urls) > 10:
            raise ValueError("Maximum 10 photos allowed")

    def _validate_time_range(self, start: datetime, end: datetime) -> None:
        if start >= end:
            raise ValueError("End time must be after start time")

    def update_title(self, title: str) -> None:
        self._validate_title(title)
        self.title = title.strip()

    def update_description(self, description: str) -> None:
        self._validate_description(description)
        self.description = description.strip()

    def update_location(self, location: Location) -> None:
        self.location = location

    def update_time(self, start: datetime, end: datetime | None = None) -> None:
        if end is not None:
            self._validate_time_range(start, end)
        self.start_time = start
        self.end_time = end

    def set_max_participants(self, value: int | None) -> None:
        if value is not None:
            self._validate_max_participants(value)
        self.max_participants = value

    def add_photo(self, url: str) -> None:
        if len(self.photo_urls) >= 10:
            raise ValueError("Maximum 10 photos allowed")
        if url not in self.photo_urls:
            self.photo_urls.append(url)

    def remove_photo(self, url: str) -> None:
        if url in self.photo_urls:
            self.photo_urls.remove(url)

    def to_dto(self) -> dict:
        return {
            "id": self.id,
            "organizer_id": self.organizer_id,
            "title": self.title,
            "description": self.description,
            "location": {
                "latitude": self.location.latitude,
                "longitude": self.location.longitude,
                "address": self.location.address,
            },
            "start_time": self.start_time,
            "end_time": self.end_time,
            "event_type": self.event_type.value,
            "max_participants": self.max_participants,
            "photo_urls": self.photo_urls,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }