# app/infrastructure/di/providers/use_cases/event.py
from dishka import Provider, Scope, provide

from app.application.use_cases.event.create_event import CreateEventUseCase
from app.application.use_cases.event.delete_event import DeleteEventUseCase
from app.application.use_cases.event.get_event import GetEventUseCase
from app.application.use_cases.event.list_events import ListEventsUseCase
from app.application.use_cases.event.update_event import UpdateEventUseCase
from app.domain.ports.repositories.event import IEventRepository


class EventUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_create_event_uc(self, repo: IEventRepository) -> CreateEventUseCase:
        return CreateEventUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_event_uc(self, repo: IEventRepository) -> GetEventUseCase:
        return GetEventUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_list_events_uc(self, repo: IEventRepository) -> ListEventsUseCase:
        return ListEventsUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_event_uc(self, repo: IEventRepository) -> UpdateEventUseCase:
        return UpdateEventUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_event_uc(self, repo: IEventRepository) -> DeleteEventUseCase:
        return DeleteEventUseCase(repo)
