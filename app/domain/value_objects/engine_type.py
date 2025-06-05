from enum import Enum


class EngineType(Enum):
    """Типы двигателей мотоциклов"""
    INLINE_2 = "inline_2"
    INLINE_3 = "inline_3"
    INLINE_4 = "inline_4"
    V_TWIN = "v_twin"
    V4 = "v4"
    SINGLE = "single"
    BOXER = "boxer"
    ELECTRIC = "electric"
