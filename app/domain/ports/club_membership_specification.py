# app/domain/ports/club_membership_specification.py

from typing import Any, Protocol


class ClubMembershipSpecificationPort(Protocol):
    """Порт для спецификаций поиска членств в мотоклубах"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...