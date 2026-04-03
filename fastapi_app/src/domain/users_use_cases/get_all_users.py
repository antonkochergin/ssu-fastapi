from typing import List
from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import User


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Получить список всех пользователей"""
        try:
            with self._database.session() as session:
                users = self._repo.get_all(session, skip, limit)
                return [User.model_validate(user) for user in users]

        except Exception as e:
            print(f"Ошибка при получении списка пользователей: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )