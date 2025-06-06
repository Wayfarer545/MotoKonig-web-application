# app/domain/value_objects/club_role.py

from enum import IntEnum


class ClubRole(IntEnum):
    """
    Роли в мотоклубе

    Чем меньше числовое значение, тем выше роль в иерархии
    """
    PRESIDENT = 0  # Президент (создатель клуба)
    VICE_PRESIDENT = 1  # Вице-президент
    SECRETARY = 2  # Секретарь
    TREASURER = 3  # Казначей
    EVENT_ORGANIZER = 4  # Организатор событий
    MODERATOR = 5  # Модератор
    SENIOR_MEMBER = 6  # Старший участник
    MEMBER = 7  # Обычный участник

    def get_display_name(self) -> str:
        """Получить отображаемое название роли"""
        display_names = {
            ClubRole.PRESIDENT: "Президент",
            ClubRole.VICE_PRESIDENT: "Вице-президент",
            ClubRole.SECRETARY: "Секретарь",
            ClubRole.TREASURER: "Казначей",
            ClubRole.EVENT_ORGANIZER: "Организатор событий",
            ClubRole.MODERATOR: "Модератор",
            ClubRole.SENIOR_MEMBER: "Старший участник",
            ClubRole.MEMBER: "Участник",
        }
        return display_names[self]

    def can_invite_members(self) -> bool:
        """Может ли роль приглашать участников"""
        return self <= ClubRole.SECRETARY

    def can_remove_members(self) -> bool:
        """Может ли роль исключать участников"""
        return self <= ClubRole.VICE_PRESIDENT

    def can_manage_roles(self) -> bool:
        """Может ли роль управлять ролями других участников"""
        return self <= ClubRole.VICE_PRESIDENT

    def can_edit_club(self) -> bool:
        """Может ли роль редактировать информацию о клубе"""
        return self <= ClubRole.SECRETARY
