# app/domain/value_objects/condition_type.py

from enum import Enum


class ConditionType(Enum):
    """Состояние товара"""
    NEW = "new"                    # Новое
    LIKE_NEW = "like_new"         # Как новое
    EXCELLENT = "excellent"        # Отличное
    GOOD = "good"                 # Хорошее
    FAIR = "fair"                 # Удовлетворительное
    POOR = "poor"                 # Плохое
    FOR_PARTS = "for_parts"       # На запчасти
    NOT_WORKING = "not_working"   # Не работает