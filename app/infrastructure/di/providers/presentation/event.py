# app/infrastructure/di/providers/presentation/event.py
from dishka import Provider, Scope, provide

from app.application.controllers.event_controller import EventController
from app.application.use_cases.event.create_event import CreateEventUseCase
from app.application.use_cases.event.delete_event import DeleteEventUseCase
from app.application.use_cases.event.get_event import GetEventUseCase
from app.application.use_cases.event.list_events import ListEventsUseCase
from app.application.use_cases.event.update_event import UpdateEventUseCase


class EventControllerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_event_controller(
            self,
            create_uc: CreateEventUseCase,
            get_uc: GetEventUseCase,
            list_uc: ListEventsUseCase,
            update_uc: UpdateEventUseCase,
            delete_uc: DeleteEventUseCase,
    ) -> EventController:
        return EventController(create_uc, get_uc, list_uc, update_uc, delete_uc)
