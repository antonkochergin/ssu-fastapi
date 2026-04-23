from passlib.context import CryptContext
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import UserUpdate, User
from fastapi_app.src.core.exeptions.exceptions import AppException, NotFoundException, ConflictError, DatabaseException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, user_data: UserUpdate) -> User:
        try:
            with self._database.session() as session:
                existing_user = self._repo.get_by_id(session, user_id)
                if not existing_user:
                    raise NotFoundException(resource="Пользователь", field="id", value=user_id)

                if user_data.username and user_data.username != existing_user.username:
                    if self._repo.get_by_username(session, user_data.username):
                        raise ConflictError(resource="User", field="username", value=user_data.username)

                if user_data.email and user_data.email != existing_user.email:
                    email_exists = session.query(self._repo.model).filter(
                        self._repo.model.email == user_data.email
                    ).first()
                    if email_exists:
                        raise ConflictError(resource="User", field="email", value=user_data.email)

                if user_data.password:
                    user_data.password = pwd_context.hash(user_data.password)

                updated_user = self._repo.update(session, user_id, user_data)

                if not updated_user:
                    raise DatabaseException(message="Не удалось обновить данные пользователя в базе")

                return User.model_validate(updated_user)

        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Внутренняя ошибка при обновлении: {str(e)}")