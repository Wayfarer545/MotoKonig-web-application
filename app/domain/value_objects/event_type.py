# app/domain/value_objects/event_type.py
from enum import Enum


class EventType(Enum):
    """Типы мероприятий"""

    PUBLIC = "public"  # Публичное событие, организованное клубом
    PRIVATE = "private"  # Приватное событие, организованное пользователем

    def get_display_name(self) -> str:
        """Получить отображаемое название типа"""
        names = {
            EventType.PUBLIC: "Публичное",
            EventType.PRIVATE: "Приватное",
        }
        return names[self]