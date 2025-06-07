# app/domain/entities/listing_category.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    pass


class ListingCategory:
    """
    Доменная сущность категории объявлений

    Инварианты:
    - Название не может быть пустым
    - Slug должен быть уникальным и валидным
    - Родительская категория не может ссылаться на саму себя
    """

    def __init__(
            self,
            *,
            category_id: UUID | None = None,
            name: str,
            slug: str,
            description: str | None = None,
            parent_id: UUID | None = None,
            icon: str | None = None,
            sort_order: int = 0,
            is_active: bool = True,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_name(name)
        self._validate_slug(slug)
        if description is not None:
            self._validate_description(description)

        self.id: UUID = category_id or uuid4()
        self.name: str = name.strip()
        self.slug: str = slug.strip().lower()
        self.description: str | None = description.strip() if description else None
        self.parent_id: UUID | None = parent_id
        self.icon: str | None = icon
        self.sort_order: int = sort_order
        self.is_active: bool = is_active
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_name(self, name: str) -> None:
        """Валидация названия"""
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty")
        if len(name.strip()) < 2:
            raise ValueError("Category name must be at least 2 characters long")
        if len(name.strip()) > 100:
            raise ValueError("Category name cannot be longer than 100 characters")

    def _validate_slug(self, slug: str) -> None:
        """Валидация slug"""
        import re
        if not slug or not slug.strip():
            raise ValueError("Category slug cannot be empty")

        clean_slug = slug.strip().lower()
        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', clean_slug):
            raise ValueError("Slug must contain only lowercase letters, numbers and hyphens")

        if len(clean_slug) < 2:
            raise ValueError("Slug must be at least 2 characters long")
        if len(clean_slug) > 50:
            raise ValueError("Slug cannot be longer than 50 characters")

    def _validate_description(self, description: str) -> None:
        """Валидация описания"""
        if len(description.strip()) > 500:
            raise ValueError("Description cannot be longer than 500 characters")

    def update_name(self, name: str) -> None:
        """Обновить название"""
        self._validate_name(name)
        self.name = name.strip()

    def update_slug(self, slug: str) -> None:
        """Обновить slug"""
        self._validate_slug(slug)
        self.slug = slug.strip().lower()

    def update_description(self, description: str | None) -> None:
        """Обновить описание"""
        if description is not None:
            self._validate_description(description)
        self.description = description.strip() if description else None

    def activate(self) -> None:
        """Активировать категорию"""
        self.is_active = True

    def deactivate(self) -> None:
        """Деактивировать категорию"""
        self.is_active = False

    def is_root_category(self) -> bool:
        """Проверить, является ли корневой категорией"""
        return self.parent_id is None

    def is_subcategory(self) -> bool:
        """Проверить, является ли подкатегорией"""
        return self.parent_id is not None

    def update_sort_order(self, sort_order: int) -> None:
        """Обновить порядок сортировки"""
        self.sort_order = sort_order

    def set_parent(self, parent_id: UUID | None) -> None:
        """Установить родительскую категорию"""
        if parent_id == self.id:
            raise ValueError("Category cannot be parent of itself")
        self.parent_id = parent_id

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "parent_id": self.parent_id,
            "icon": self.icon,
            "sort_order": self.sort_order,
            "is_active": self.is_active,
            "is_root_category": self.is_root_category(),
            "is_subcategory": self.is_subcategory(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }