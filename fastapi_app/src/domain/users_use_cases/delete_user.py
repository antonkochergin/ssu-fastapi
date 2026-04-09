from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.exeptions import AppException, NotFoundException, DatabaseException

class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing_user = self._repo.get_by_id(session, user_id)
                if not existing_user:
                    raise NotFoundException(resource="Пользователь", field="id", value=user_id)

                deleted = self._repo.delete(session, user_id)
                if not deleted:
                    raise DatabaseException(message="Не удалось удалить пользователя из базы")

                return {"message": f"Пользователь с ID {user_id} успешно удален"}
        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=str(e))