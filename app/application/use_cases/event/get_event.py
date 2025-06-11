# app/application/use_cases/event/get_event.py
from app.domain.entities.event import Event
from app.domain.ports.repositories.event import IEventRepository
from app.domain.ports.specs.event import EventSpecificationPort


class GetEventUseCase:
    """Use case для получения мероприятия"""

    def __init__(self, repo: IEventRepository):
        self.repo = repo

    async def execute(self, spec: EventSpecificationPort) -> Event | None:
        return await self.repo.get(spec)