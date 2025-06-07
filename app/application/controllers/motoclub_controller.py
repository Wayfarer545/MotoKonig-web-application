# app/application/controllers/motoclub_controller.py

from uuid import UUID

from app.application.exceptions import BadRequestError, NotFoundError
from app.application.use_cases.club_invitation.invite_user import (
    InviteUserToClubUseCase,
)
from app.application.use_cases.club_membership.join_club import JoinClubUseCase
from app.application.use_cases.moto_club.create_club import CreateMotoClubUseCase
from app.application.use_cases.moto_club.delete_club import DeleteMotoClubUseCase
from app.application.use_cases.moto_club.get_club import GetMotoClubUseCase
from app.application.use_cases.moto_club.list_clubs import ListMotoClubsUseCase
from app.application.use_cases.moto_club.update_club import UpdateMotoClubUseCase
from app.domain.value_objects.club_role import ClubRole
from app.infrastructure.specs.moto_club.club_by_id import MotoClubById
from app.infrastructure.specs.moto_club.club_filter import MotoClubFilter


class MotoClubController:
    """Контроллер для управления мотоклубами"""

    def __init__(
            self,
            create_uc: CreateMotoClubUseCase,
            get_uc: GetMotoClubUseCase,
            list_uc: ListMotoClubsUseCase,
            update_uc: UpdateMotoClubUseCase,
            delete_uc: DeleteMotoClubUseCase,
            join_uc: JoinClubUseCase,
            invite_uc: InviteUserToClubUseCase,
    ):
        self.create_uc = create_uc
        self.get_uc = get_uc
        self.list_uc = list_uc
        self.update_uc = update_uc
        self.delete_uc = delete_uc
        self.join_uc = join_uc
        self.invite_uc = invite_uc

    async def create_club(
            self,
            name: str,
            president_id: UUID,
            description: str | None = None,
            is_public: bool = True,
            max_members: int | None = None,
            location: str | None = None,
            website: str | None = None,
    ) -> dict:
        """Создать новый мотоклуб"""
        try:
            club = await self.create_uc.execute(
                name=name,
                president_id=president_id,
                description=description,
                is_public=is_public,
                max_members=max_members,
                location=location,
                website=website,
            )
            return club.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def get_club_by_id(self, club_id: UUID) -> dict:
        """Получить мотоклуб по ID"""
        spec = MotoClubById(club_id)
        club = await self.get_uc.execute(spec)

        if not club:
            raise NotFoundError("MotoClub not found")

        return club.to_dto()

    async def list_clubs(
            self,
            public_only: bool = False,
            active_only: bool = True,
            name: str | None = None,
            location: str | None = None,
    ) -> list[dict]:
        """Получить список мотоклубов"""
        spec = MotoClubFilter(
            name=name,
            location=location,
            is_public=True if public_only else None,
            is_active=active_only,
        )
        clubs = await self.list_uc.execute(spec)
        return [club.to_dto() for club in clubs]

    async def update_club(
            self,
            club_id: UUID,
            name: str | None = None,
            description: str | None = None,
            is_public: bool | None = None,
            max_members: int | None = None,
            location: str | None = None,
            website: str | None = None,
            avatar_url: str | None = None,
    ) -> dict:
        """Обновить мотоклуб"""
        try:
            updated = await self.update_uc.execute(
                club_id=club_id,
                name=name,
                description=description,
                is_public=is_public,
                max_members=max_members,
                location=location,
                website=website,
                avatar_url=avatar_url,
            )

            if not updated:
                raise NotFoundError("MotoClub not found")

            return updated.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def delete_club(self, club_id: UUID) -> None:
        """Удалить мотоклуб"""
        success = await self.delete_uc.execute(club_id)
        if not success:
            raise NotFoundError("MotoClub not found")

    async def join_club(
            self,
            club_id: UUID,
            user_id: UUID,
            role: ClubRole = ClubRole.MEMBER
    ) -> dict:
        """Вступить в мотоклуб"""
        try:
            membership = await self.join_uc.execute(
                club_id=club_id,
                user_id=user_id,
                role=role
            )
            return membership.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def invite_user(
            self,
            club_id: UUID,
            inviter_id: UUID,
            invitee_id: UUID,
            invited_role: ClubRole = ClubRole.MEMBER,
            message: str | None = None
    ) -> dict:
        """Пригласить пользователя в мотоклуб"""
        try:
            invitation = await self.invite_uc.execute(
                club_id=club_id,
                inviter_id=inviter_id,
                invitee_id=invitee_id,
                invited_role=invited_role,
                message=message
            )
            return invitation.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex
