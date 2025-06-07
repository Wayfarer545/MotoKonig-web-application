# app/domain/ports/user.py

from typing import Any, Protocol


class UserSpecificationPort(Protocol):
    def to_query(self, base_query: Any) -> Any:
        ...
