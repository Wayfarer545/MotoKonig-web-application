# app/presentation/routers/event.py
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Request, status

from app.application.controllers.event_controller import EventController
from app.application.exceptions import BadRequestError, NotFoundError
from app.domain.ports.services.token import TokenServicePort
from app.domain.value_objects.event_type import EventType
from app.presentation.dependencies.auth import get_current_user_dishka
from app.presentation.schemas.event import (
    CreateEventSchema,
    EventResponseSchema,
    UpdateEventSchema,
)

router = APIRouter(route_class=DishkaRoute)


@router.post("/", response_model=EventResponseSchema, status_code=201)
async def create_event(
        request: Request,
        dto: CreateEventSchema,
        controller: FromDishka[EventController],
        token_service: FromDishka[TokenServicePort],
):
    current_user = await get_current_user_dishka(request, token_service)
    try:
        event = await controller.create_event(
            organizer_id=current_user["user_id"],
            title=dto.title,
            description=dto.description,
            location=dto.location.to_vo(),
            start_time=dto.start_time,
            end_time=dto.end_time,
            event_type=dto.event_type,
            max_participants=dto.max_participants,
            photo_urls=dto.photo_urls,
        )
        return event
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex)
        ) from ex


@router.get("/{event_id}", response_model=EventResponseSchema)
async def get_event(
        event_id: UUID,
        controller: FromDishka[EventController],
):
    try:
        return await controller.get_event_by_id(event_id)
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex


@router.get("/", response_model=list[EventResponseSchema])
async def list_events(
        controller: FromDishka[EventController],
        organizer_id: UUID | None = None,
        event_type: EventType | None = None,
        start_from: str | None = None,
        start_to: str | None = None,
        location_query: str | None = None,
):
    import datetime as dt
    sf = dt.datetime.fromisoformat(start_from) if start_from else None
    st = dt.datetime.fromisoformat(start_to) if start_to else None
    events = await controller.list_events(
        organizer_id=organizer_id,
        event_type=event_type,
        start_from=sf,
        start_to=st,
        location_query=location_query,
    )
    return events


@router.put("/{event_id}", response_model=EventResponseSchema)
async def update_event(
        request: Request,
        event_id: UUID,
        dto: UpdateEventSchema,
        controller: FromDishka[EventController],
        token_service: FromDishka[TokenServicePort],
):
    await get_current_user_dishka(request, token_service)
    try:
        updated = await controller.update_event(
            event_id=event_id,
            title=dto.title,
            description=dto.description,
            location=dto.location.to_vo() if dto.location else None,
            start_time=dto.start_time,
            end_time=dto.end_time,
            event_type=dto.event_type,
            max_participants=dto.max_participants,
            photo_urls=dto.photo_urls,
        )
        return updated
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
    except BadRequestError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex)
        ) from ex


@router.delete("/{event_id}", status_code=204)
async def delete_event(
        request: Request,
        event_id: UUID,
        controller: FromDishka[EventController],
        token_service: FromDishka[TokenServicePort],
):
    await get_current_user_dishka(request, token_service)
    try:
        await controller.delete_event(event_id)
    except NotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
