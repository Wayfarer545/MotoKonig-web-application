# app/infrastructure/models/media_file.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.file_type import FileType

__all__ = ["MediaFile"]

if TYPE_CHECKING:
    from .user import User


class MediaFile(UUIDAuditBase):
    """SQLAlchemy модель медиафайла"""

    __tablename__ = "media_files"

    # Связь с владельцем
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    owner: Mapped["User"] = relationship("User", lazy="selectin")

    # Информация о файле
    file_type: Mapped[FileType] = mapped_column(
        SQLEnum(FileType, name="file_type", native_enum=False),
        nullable=False,
        index=True
    )
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_key: Mapped[str] = mapped_column(String(500), nullable=False, unique=True, index=True)
    bucket: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Метаданные файла
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)

    # Настройки доступа
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)

    # Дополнительные метаданные (JSON)
    file_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)
