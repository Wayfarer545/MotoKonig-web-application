# app/application/use_cases/auth/login.py


from typing import Optional, Tuple
from uuid import UUID

from adapters.specifications.user_specs.user_by_id import UserById
from app.domain.ports.auth_service import AuthService
from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.password_service import PasswordService
from app.domain.ports.token_service import TokenService
from app.domain.entities.user import User
from app.adapters.specifications.user_specs.user_by_name import UserByName


class AuthServiceImpl(AuthService):
    def __init__(
            self,
            user_repo: IUserRepository,
            pwd_service: PasswordService,
            token_service: TokenService
    ):
        self.user_repo = user_repo
        self.pwd_service = pwd_service
        self.token_service = token_service

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repo.get(UserByName(username))
        if not user:
            return None

        if not await self.pwd_service.verify(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        return user

    async def create_tokens(self, user: User) -> Tuple[str, str]:
        additional_claims = {
            "username": user.username,
            "role": user.role.name
        }

        access_token = await self.token_service.create_access_token(
            str(user.id),
            additional_claims
        )
        refresh_token = await self.token_service.create_refresh_token(str(user.id))

        return access_token, refresh_token

    async def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        payload = await self.token_service.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")
        user = await self.user_repo.get(UserById(UUID(user_id)))

        if not user or not user.is_active:
            return None

        # Отзываем старый refresh token
        await self.token_service.revoke_token(refresh_token)

        # Создаём новую пару токенов
        return await self.create_tokens(user)

    async def logout(self, access_token: str, refresh_token: str) -> None:
        # Добавляем оба токена в блэклист
        await self.token_service.revoke_token(access_token)
        await self.token_service.revoke_token(refresh_token)