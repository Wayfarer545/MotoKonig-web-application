from enum import Enum


class MotorcycleType(Enum):
    """Типы мотоциклов"""
    SPORT = "sport"  # Спортбайк
    NAKED = "naked"  # Нейкед
    TOURING = "touring"  # Турер
    CRUISER = "cruiser"  # Круизёр
    CHOPPER = "chopper"  # Чоппер
    ADVENTURE = "adventure"  # Эндуро/адвенчер
    DIRT_BIKE = "dirt_bike"  # Кроссовый
    SUPERMOTO = "supermoto"  # Супермото
    CAFE_RACER = "cafe_racer"  # Кафе рейсер
    SCRAMBLER = "scrambler"  # Скрамблер
    SCOOTER = "scooter"  # Скутер
    TRIKE = "trike"  # Трайк
    ELECTRIC = "electric"  # Электрический
