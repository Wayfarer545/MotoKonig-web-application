# app/domain/ports/moto_club.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.moto_club import MotoClub
from app.domain.ports.specs.moto_club import MotoClubSpecificationPort


class IMotoClubRepository(Protocol):
    """Порт репозитория мотоклубов"""

    async def add(self, club: MotoClub) -> MotoClub:
        """Добавить новый мотоклуб"""
        ...

    async def get(self, spec: MotoClubSpecificationPort) -> MotoClub | None:
        """Получить мотоклуб по спецификации"""
        ...

    async def get_list(self, spec: MotoClubSpecificationPort | None = None) -> list[MotoClub]:
        """Получить список мотоклубов по спецификации"""
        ...

    async def update(self, club: MotoClub) -> MotoClub:
        """Обновить мотоклуб"""
        ...

    async def delete(self, club_id: UUID) -> bool:
        """Удалить мотоклуб"""
        ...
