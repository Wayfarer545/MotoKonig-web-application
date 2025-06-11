# app/domain/value_objects/ride_difficulty.py
from enum import IntEnum


class RideDifficulty(IntEnum):
    """Сложность маршрута"""
    EASY = 1
    MODERATE = 2
    HARD = 3
    EXTREME = 4
    LEGENDARY = 5
