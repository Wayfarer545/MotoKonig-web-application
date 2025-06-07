# app/domain/ports/club_invitation.py

from typing import Any, Protocol


class ClubInvitationSpecificationPort(Protocol):
    """Порт для спецификаций поиска приглашений в мотоклубы"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...
