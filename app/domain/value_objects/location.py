# app/domain/value_objects/location.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    """Value object, представляющий геолокацию"""

    latitude: float
    longitude: float
    address: str | None = None

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        if self.address is not None and len(self.address.strip()) > 200:
            raise ValueError("Address cannot be longer than 200 characters")
        if self.address is not None and not self.address.strip():
            object.__setattr__(self, "address", None)

    def __str__(self) -> str:
        if self.address:
            return f"{self.address} ({self.latitude}, {self.longitude})"
        return f"{self.latitude}, {self.longitude}"
