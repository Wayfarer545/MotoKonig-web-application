# app/domain/entities/listing_favorite.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    pass


class ListingFavorite:
    """
    Доменная сущность избранного объявления

    Инварианты:
    - Пользователь может добавить объявление в избранное только один раз
    - Нельзя добавить свое собственное объявление в избранное
    """

    def __init__(
            self,
            *,
            favorite_id: UUID | None = None,
            user_id: UUID,
            listing_id: UUID,
            created_at: datetime | None = None,
    ):
        self.id: UUID = favorite_id or uuid4()
        self.user_id: UUID = user_id
        self.listing_id: UUID = listing_id
        self.created_at: datetime = created_at or datetime.utcnow()

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "listing_id": self.listing_id,
            "created_at": self.created_at,
        }
