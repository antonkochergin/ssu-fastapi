from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import User
from fastapi_app.src.core.exeptions.exceptions import AppException, NotFoundException, DatabaseException

class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> User:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)
                if not user:
                    raise NotFoundException(resource="Пользователь", field="username", value=username)
                return User.model_validate(user)
        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=str(e))