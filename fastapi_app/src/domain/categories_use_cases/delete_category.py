from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository
from fastapi_app.src.core.exeptions.exceptions import AppException, NotFoundException, DatabaseException

class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing_category = self._repo.get_by_id(session, category_id)
                if not existing_category:
                    raise NotFoundException(resource="Категория", field="id", value=category_id)

                deleted = self._repo.delete(session, category_id)
                if not deleted:
                    raise DatabaseException(message="Не удалось удалить категорию")

                return {"message": f"Категория с ID {category_id} успешно удалена"}

        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Внутренняя ошибка сервера при удалении: {str(e)}")