from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository
from fastapi_app.src.schemas.categories import Category
from fastapi_app.src.core.exeptions.exceptions import AppException, NotFoundException, DatabaseException

class GetCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Category:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)
                if not category:
                    raise NotFoundException(resource="Категория", field="id", value=category_id)
                return Category.model_validate(category)
        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка получения категории: {str(e)}")