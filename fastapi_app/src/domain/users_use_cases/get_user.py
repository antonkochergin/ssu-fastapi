from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import User
from fastapi_app.src.exeptions import AppException, NotFoundException, DatabaseException

class GetUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> User:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_id(session, user_id)
                if not user:
                    raise NotFoundException(resource="Пользователь", field="id", value=user_id)
                return User.model_validate(user)
        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=str(e))