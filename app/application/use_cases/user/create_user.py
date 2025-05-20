# app/application/use_cases/user/create_user.py

from app.domain.entities.user import User, UserRole
from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.password_service import PasswordService


class CreateUserUseCase:
    def __init__(self, repo: IUserRepository, pwd_service: PasswordService):
        self.repo = repo
        self.pwd_service = pwd_service

    async def execute(
        self,
        username: str,
        raw_password: str,
        role: UserRole = UserRole.USER,
    ) -> User:
        password_hash = await self.pwd_service.hash(raw_password)
        user = User(username=username, password_hash=password_hash, role=role)
        return await self.repo.add(user)
