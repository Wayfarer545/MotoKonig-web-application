# app/domain/entities/moto_club.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    pass


class MotoClub:
    """
    Доменная сущность мотоклуба

    Инварианты:
    - Название клуба не может быть пустым
    - Описание не может быть слишком длинным
    - У клуба должен быть президент (создатель)
    - Клуб может быть публичным или приватным
    """

    def __init__(
            self,
            *,
            club_id: UUID | None = None,
            name: str,
            description: str | None = None,
            president_id: UUID,
            is_public: bool = True,
            max_members: int | None = None,
            location: str | None = None,
            website: str | None = None,
            founded_date: datetime | None = None,
            avatar_url: str | None = None,
            is_active: bool = True,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_name(name)
        if description is not None:
            self._validate_description(description)
        if max_members is not None:
            self._validate_max_members(max_members)
        if location is not None:
            self._validate_location(location)

        self.id: UUID = club_id or uuid4()
        self.name: str = name.strip()
        self.description: str | None = description.strip() if description else None
        self.president_id: UUID = president_id
        self.is_public: bool = is_public
        self.max_members: int | None = max_members
        self.location: str | None = location.strip() if location else None
        self.website: str | None = website.strip() if website else None
        self.founded_date: datetime | None = founded_date or datetime.utcnow()
        self.avatar_url: str | None = avatar_url
        self.is_active: bool = is_active
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_name(self, name: str) -> None:
        """Валидация названия клуба"""
        if not name or not name.strip():
            raise ValueError("Club name cannot be empty")
        if len(name.strip()) < 3:
            raise ValueError("Club name must be at least 3 characters long")
        if len(name.strip()) > 100:
            raise ValueError("Club name cannot be longer than 100 characters")

    def _validate_description(self, description: str) -> None:
        """Валидация описания клуба"""
        if len(description.strip()) > 2000:
            raise ValueError("Club description cannot be longer than 2000 characters")

    def _validate_max_members(self, max_members: int) -> None:
        """Валидация максимального количества участников"""
        if max_members <= 0:
            raise ValueError("Max members must be positive")
        if max_members > 10000:
            raise ValueError("Max members cannot exceed 10000")

    def _validate_location(self, location: str) -> None:
        """Валидация локации"""
        if len(location.strip()) > 200:
            raise ValueError("Location cannot be longer than 200 characters")

    def update_name(self, name: str) -> None:
        """Обновить название клуба"""
        self._validate_name(name)
        self.name = name.strip()

    def update_description(self, description: str | None) -> None:
        """Обновить описание клуба"""
        if description is not None:
            self._validate_description(description)
        self.description = description.strip() if description else None

    def update_location(self, location: str | None) -> None:
        """Обновить локацию клуба"""
        if location is not None:
            self._validate_location(location)
        self.location = location.strip() if location else None

    def set_max_members(self, max_members: int | None) -> None:
        """Установить максимальное количество участников"""
        if max_members is not None:
            self._validate_max_members(max_members)
        self.max_members = max_members

    def make_public(self) -> None:
        """Сделать клуб публичным"""
        self.is_public = True

    def make_private(self) -> None:
        """Сделать клуб приватным"""
        self.is_public = False

    def deactivate(self) -> None:
        """Деактивировать клуб"""
        self.is_active = False

    def activate(self) -> None:
        """Активировать клуб"""
        self.is_active = True

    def transfer_presidency(self, new_president_id: UUID) -> None:
        """Передать президентство другому участнику"""
        self.president_id = new_president_id

    def update_avatar(self, avatar_url: str | None) -> None:
        """Обновить аватар клуба"""
        self.avatar_url = avatar_url

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "president_id": self.president_id,
            "is_public": self.is_public,
            "max_members": self.max_members,
            "location": self.location,
            "website": self.website,
            "founded_date": self.founded_date,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
