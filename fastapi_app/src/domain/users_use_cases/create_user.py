from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import UserCreate, User
from fastapi_app.src.core.exeptions.exceptions import AppException, ConflictError, DatabaseException
from passlib.context import CryptContext
from src.resources.auth import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> User:
        """Регистрации пользователя"""
        try:
            with self._database.session() as session:
                if self._repo.get_by_username(session, user_data.username):
                    raise ConflictError(
                        resource="User",
                        field="username",
                        value=user_data.username
                    )

                hashed_password = get_password_hash(user_data.password)
                user_data.password = hashed_password

                new_user = self._repo.create(
                    session=session,
                    user_data=user_data,
                    hashed_password=hashed_password
                )

                return User.model_validate(new_user)

        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка регистрации: {str(e)}")