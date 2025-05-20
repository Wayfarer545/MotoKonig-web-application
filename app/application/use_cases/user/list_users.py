# app/application/use_cases/user/list_users.py

from typing import List
from app.domain.entities.user import User
from app.domain.ports.user_repository import IUserRepository

class ListUsersUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self) -> List[User]:
        return await self.repo.get_list()
