# app/domain/value_objects/listing_category.py

from enum import Enum


class ListingCategory(Enum):
    """Категории товаров в маркетплейсе"""
    MOTORCYCLES = "motorcycles"  # Мотоциклы
    PARTS = "parts"  # Запчасти
    EQUIPMENT = "equipment"  # Экипировка
    SERVICES = "services"  # Услуги
    ACCESSORIES = "accessories"  # Аксессуары

    def get_display_name(self) -> str:
        """Получить отображаемое название категории"""
        display_names = {
            ListingCategory.MOTORCYCLES: "Мотоциклы",
            ListingCategory.PARTS: "Запчасти",
            ListingCategory.EQUIPMENT: "Экипировка",
            ListingCategory.SERVICES: "Услуги",
            ListingCategory.ACCESSORIES: "Аксессуары",
        }
        return display_names[self]

    def get_description(self) -> str:
        """Получить описание категории"""
        descriptions = {
            ListingCategory.MOTORCYCLES: "Продажа мотоциклов, скутеров и другой мототехники",
            ListingCategory.PARTS: "Запчасти и комплектующие для мотоциклов",
            ListingCategory.EQUIPMENT: "Защитная экипировка, шлемы, куртки, ботинки",
            ListingCategory.SERVICES: "Ремонт, техобслуживание, кастомизация",
            ListingCategory.ACCESSORIES: "Аксессуары, тюнинг, декор",
        }
        return descriptions[self]
