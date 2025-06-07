# app/domain/value_objects/listing_type.py

from enum import Enum


class ListingType(Enum):
    """Типы объявлений"""
    SALE = "sale"           # Продажа
    SERVICE = "service"     # Услуга
    WANTED = "wanted"       # Куплю
    EXCHANGE = "exchange"   # Обмен
    RENT = "rent"          # Аренда
    FREE = "free"          # Отдам даром