# app/domain/value_objects/file_type.py

from enum import Enum


class FileType(Enum):
    """Типы файлов в системе"""
    AVATAR = "avatar"
    MOTORCYCLE_PHOTO = "motorcycle_photo"
    EVENT_PHOTO = "event_photo"
    DOCUMENT = "document"
    TEMP = "temp"

    def get_bucket_name(self) -> str:
        """Получить название бакета для типа файла"""
        bucket_mapping = {
            FileType.AVATAR: "avatars",
            FileType.MOTORCYCLE_PHOTO: "motorcycles",
            FileType.EVENT_PHOTO: "events",
            FileType.DOCUMENT: "documents",
            FileType.TEMP: "temp"
        }
        return bucket_mapping[self]

    def get_max_size_mb(self) -> int:
        """Получить максимальный размер файла в MB"""
        size_mapping = {
            FileType.AVATAR: 5,  # 5MB
            FileType.MOTORCYCLE_PHOTO: 10,  # 10MB
            FileType.EVENT_PHOTO: 10,  # 10MB
            FileType.DOCUMENT: 25,  # 25MB
            FileType.TEMP: 50  # 50MB
        }
        return size_mapping[self]

    def get_allowed_content_types(self) -> list[str]:
        """Получить разрешённые MIME типы"""
        content_type_mapping = {
            FileType.AVATAR: [
                "image/jpeg", "image/png", "image/webp"
            ],
            FileType.MOTORCYCLE_PHOTO: [
                "image/jpeg", "image/png", "image/webp"
            ],
            FileType.EVENT_PHOTO: [
                "image/jpeg", "image/png", "image/webp"
            ],
            FileType.DOCUMENT: [
                "application/pdf", "image/jpeg", "image/png"
            ],
            FileType.TEMP: [
                "image/jpeg", "image/png", "image/webp", "application/pdf"
            ]
        }
        return content_type_mapping[self]
