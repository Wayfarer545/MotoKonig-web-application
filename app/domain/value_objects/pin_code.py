import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PinCode:
    """Value object для PIN-кода"""
    value: str

    def __post_init__(self):
        if not re.match(r'^\d{4,6}$', self.value):
            raise ValueError("PIN must be 4-6 digits")

    def __str__(self) -> str:
        return self.value
