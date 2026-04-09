from typing import List
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import User
from fastapi_app.src.exeptions import AppException, DatabaseException

class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, skip: int = 0, limit: int = 100) -> List[User]:
        try:
            with self._database.session() as session:
                users = self._repo.get_all(session, skip, limit)
                return [User.model_validate(u) for u in users]
        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=str(e))