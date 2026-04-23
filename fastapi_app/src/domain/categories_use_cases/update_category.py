import re
import logging
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository
from fastapi_app.src.schemas.categories import CategoryUpdate, Category
from fastapi_app.src.core.exeptions.exceptions import AppException, NotFoundException, DatabaseException

logger = logging.getLogger(__name__)

class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    def _generate_slug(self, title: str) -> str:
        slug = title.lower().replace(' ', '-')
        slug = re.sub(r'[^a-zA-Z0-9-]', '', slug)
        return slug[:32]

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> Category:
        try:
            with self._database.session() as session:
                existing_category = self._repo.get_by_id(session, category_id)
                if not existing_category:
                    raise NotFoundException(resource="Категория", field="id", value=category_id)

                if category_data.title and not category_data.slug:
                    category_data.slug = self._generate_slug(category_data.title)

                updated_category = self._repo.update(session, category_id, category_data)
                if not updated_category:
                    raise DatabaseException(message="Не удалось обновить категорию")

                return Category.model_validate(updated_category)

        except AppException:
            raise
        except Exception as e:
            logger.error(f"Ошибка обновления категории: {e}")
            raise DatabaseException(message="Внутренняя ошибка сервера при обновлении")