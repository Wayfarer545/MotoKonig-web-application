# app/domain/ports/social_link_specification.py

from typing import Any, Protocol


class SocialLinkSpecificationPort(Protocol):
    """Порт для спецификаций поиска социальных ссылок"""

    def to_query(self, base_query: Any) -> Any:
        """Преобразовать спецификацию в SQL запрос"""
        ...