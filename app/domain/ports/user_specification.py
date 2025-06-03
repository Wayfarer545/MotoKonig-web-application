# app/domain/ports/user_specification.py

from typing import Protocol
from typing_extensions import Any


class UserSpecificationPort(Protocol):
    def to_query(self, base_query: Any) -> Any:
        ...
