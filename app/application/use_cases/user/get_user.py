# app/application/use_cases/user/get_user.py

from app.domain.entities.user import User
from domain.ports.repositories.user_repository import IUserRepository
from domain.ports.specs.user import UserSpecificationPort


class GetUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, user_spec: UserSpecificationPort) -> User | None:
        return await self.repo.get(user_spec)
