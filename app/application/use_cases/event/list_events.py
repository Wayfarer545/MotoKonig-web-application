# app/application/use_cases/event/list_events.py
from app.domain.entities.event import Event
from app.domain.ports.repositories.event import IEventRepository
from app.domain.ports.specs.event import EventSpecificationPort


class ListEventsUseCase:
    """Use case для списка мероприятий"""

    def __init__(self, repo: IEventRepository):
        self.repo = repo

    async def execute(self, spec: EventSpecificationPort | None = None) -> list[Event]:
        return await self.repo.get_list(spec)