from passlib.context import CryptContext

from app.domain.ports.password_service import PasswordService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordServiceImpl(PasswordService):
    async def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify(self, password: str, hash: str) -> bool:
        return pwd_context.verify(password, hash)
