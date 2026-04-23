import logging
from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from pydantic import SecretStr

from src.core.exceptions.auth_exceptions import CredentialsException
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repository import UsersRepository
from src.resources.auth import oauth2_scheme
from src.schemas.users import User as UserSchema

logger = logging.getLogger(__name__)

# Секретный ключ для подписи JWT
SECRET_AUTH_KEY = SecretStr("aF75A92Cd9s10KGL4nLdt1r85XRtZ7APNO6NheGeKdRBhhc9oObQywxmqPF")
AUTH_ALGORITHM = "HS256"
AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"


class AuthService:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserSchema:
        _database = database
        _repo = UsersRepository()

        try:
            # Декодируем токен
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[AUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                logger.error(f"Token missing 'sub' claim: {token}")
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        except JWTError as e:
            logger.error(f"JWT decode error: {e}")
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        try:
            # Ищем пользователя по username из токена
            with _database.session() as session:
                user = _repo.get_by_username(session=session, username=username)
        except UserNotFoundException:
            logger.error(f"User not found for username from token: {username}")
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        return UserSchema.model_validate(obj=user)