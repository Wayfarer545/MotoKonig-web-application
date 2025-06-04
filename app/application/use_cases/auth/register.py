# app/application/use_cases/auth/register.py

from app.domain.entities.user import User, UserRole
from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.password_service import PasswordService
from app.adapters.specifications.user_specs.user_by_name import UserByName


class RegisterUseCase:
    """Use case для регистрации нового пользователя"""

    def __init__(
            self,
            user_repo: IUserRepository,
            pwd_service: PasswordService
    ):
        self.user_repo = user_repo
        self.pwd_service = pwd_service

    async def execute(
            self,
            username: str,
            password: str,
            email: str | None = None  # Подготовка для будущего
    ) -> User:
        """
        Регистрация нового пользователя

        - Первый пользователь становится админом
        - Проверка уникальности username
        """
        # Проверяем, существует ли пользователь
        existing = await self.user_repo.get(UserByName(username))
        if existing:
            raise ValueError("Username already taken")

        # Определяем роль - первый пользователь = админ
        all_users = await self.user_repo.get_list()
        role = UserRole.ADMIN if len(all_users) == 0 else UserRole.USER

        # Хешируем пароль
        password_hash = await self.pwd_service.hash(password)

        # Создаём пользователя
        user = User(
            username=username,
            password_hash=password_hash,
            role=role
        )

        return await self.user_repo.add(user)