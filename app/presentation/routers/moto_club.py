# app/presentation/routers/moto_club.py
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Request, status

from app.application.controllers.moto_club_controller import MotoClubController
from app.application.exceptions import BadRequestError, NotFoundError
from app.domain.ports.token_service import TokenServicePort
from app.domain.value_objects.club_role import ClubRole
from app.domain.value_objects.user_role import UserRole
from app.presentation.middleware.auth import check_role, get_current_user_dishka
from app.presentation.schemas.moto_club import (
    CreateMotoClubSchema,
    InviteUserSchema,
    JoinClubSchema,
    MotoClubResponseSchema,
    UpdateMotoClubSchema,
    ClubMembershipResponseSchema,
    ClubInvitationResponseSchema,
)

router = APIRouter(route_class=DishkaRoute)


@router.post("/", response_model=MotoClubResponseSchema, status_code=201)
async def create_moto_club(
        request: Request,
        dto: CreateMotoClubSchema,
        controller: FromDishka[MotoClubController],
        token_service: FromDishka[TokenServicePort]
):
    """Создать новый мотоклуб"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        club = await controller.create_club(
            name=dto.name,
            president_id=current_user["user_id"],
            description=dto.description,
            is_public=dto.is_public,
            max_members=dto.max_members,
            location=dto.location,
            website=dto.website,
        )
        return club
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.get("/", response_model=list[MotoClubResponseSchema])
async def list_moto_clubs(
        request: Request,
        controller: FromDishka[MotoClubController],
        token_service: FromDishka[TokenServicePort],
        name: str | None = None,
        location: str | None = None,
        public_only: bool = False,
        active_only: bool = True
):
    """Получить список мотоклубов"""
    current_user = await get_current_user_dishka(request, token_service)

    # Обычные пользователи могут видеть только публичные клубы
    if current_user["role"] == UserRole.USER:
        public_only = True

    clubs = await controller.list_clubs(
        public_only=public_only,
        active_only=active_only,
        name=name,
        location=location
    )
    return clubs


@router.get("/{club_id}", response_model=MotoClubResponseSchema)
async def get_moto_club(
        request: Request,
        club_id: UUID,
        controller: FromDishka[MotoClubController],
        token_service: FromDishka[TokenServicePort]
):
    """Получить мотоклуб по ID"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        club = await controller.get_club_by_id(club_id)

        # Проверяем права доступа к приватным клубам
        if not club["is_public"] and current_user["role"] == UserRole.USER:
            # TODO: Проверить, является ли пользователь участником клуба
            pass

        return club
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.put("/{club_id}", response_model=MotoClubResponseSchema)
async def update_moto_club(
        request: Request,
        club_id: UUID,
        dto: UpdateMotoClubSchema,
        controller: FromDishka[MotoClubController],
        token_service: FromDishka[TokenServicePort]
):
    """Обновить мотоклуб"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала получаем клуб для проверки прав
        existing_club = await controller.get_club_by_id(club_id)

        # Проверяем права доступа
        can_edit = (
                current_user["role"] in [UserRole.ADMIN, UserRole.OPERATOR] or
                str(current_user["user_id"]) == str(existing_club["president_id"])
        )

        if not can_edit:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to edit this club"
            )

        club = await controller.update_club(
            club_id=club_id,
            name=dto.name,
            description=dto.description,
            is_public=dto.is_public,
            max_members=dto.max_members,
            location=dto.location,
            website=dto.website,
            avatar_url=dto.avatar_url,
        )
        return club
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.delete("/{club_id}", status_code=204)
async def delete_moto_club(
        request: Request,
        club_id: UUID,
        controller: FromDishka[MotoClubController],
        token_service: FromDishka[TokenServicePort]
):
    """Удалить мотоклуб"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        # Сначала получаем клуб для проверки прав
        existing_club = await controller.get_club_by_id(club_id)

        # Только админы и президент клуба могут удалить клуб
        can_delete = (
                current_user["role"] == UserRole.ADMIN or
                str(current_user["user_id"]) == str(existing_club["president_id"])
        )

        if not can_delete:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only club president or admin can delete the club"
            )

        await controller.delete_club(club_id)
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        ) from ex


@router.post("/{club_id}/join", response_model=ClubMembershipResponseSchema)
async def join_moto_club(
        request: Request,
        club_id: UUID,
        dto: JoinClubSchema,
        controller: FromDishka[MotoClubController],
        token_service: FromDishka[TokenServicePort]
):
    """Вступить в мотоклуб"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        membership = await controller.join_club(
            club_id=club_id,
            user_id=current_user["user_id"],
            role=dto.role if dto.role else ClubRole.MEMBER
        )
        return membership
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex


@router.post("/{club_id}/invite", response_model=ClubInvitationResponseSchema)
async def invite_user_to_club(
        request: Request,
        club_id: UUID,
        dto: InviteUserSchema,
        controller: FromDishka[MotoClubController],
        token_service: FromDishka[TokenServicePort]
):
    """Пригласить пользователя в мотоклуб"""
    current_user = await get_current_user_dishka(request, token_service)

    try:
        invitation = await controller.invite_user(
            club_id=club_id,
            inviter_id=current_user["user_id"],
            invitee_id=dto.invitee_id,
            invited_role=dto.invited_role if dto.invited_role else ClubRole.MEMBER,
            message=dto.message
        )
        return invitation
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        ) from ex
