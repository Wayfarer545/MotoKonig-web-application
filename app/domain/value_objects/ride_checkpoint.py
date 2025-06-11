# app/domain/value_objects/ride_checkpoint.py

from datetime import datetime

__all__ = ["RideCheckpoint"]


class RideCheckpoint:
    """
    Value Object контрольной точки маршрута

    Инварианты:
    - Широта должна быть от -90 до 90
    - Долгота должна быть от -180 до 180
    """

    def __init__(
            self,
            *,
            latitude: float,
            longitude: float,
            name: str | None = None,
            reached_at: datetime | None = None
    ):
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.latitude = latitude
        self.longitude = longitude
        self.name = name.strip() if name else None
        self.reached_at = reached_at

    def __eq__(self, other):
        if not isinstance(other, RideCheckpoint):
            return NotImplemented
        return (
                self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.name == other.name
        )

    def __repr__(self):
        return f"RideCheckpoint(lat={self.latitude}, lng={self.longitude}, name={self.name})"
