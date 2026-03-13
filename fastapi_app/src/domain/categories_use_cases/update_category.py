from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository
from fastapi_app.src.schemas.categories import CategoryUpdate, Category
import re


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
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с ID {category_id} не найдена"
                    )

                # Генерируем slug если указан title
                if category_data.title and not category_data.slug:
                    category_data.slug = self._generate_slug(category_data.title)

                # Обновляем категорию без проверки уникальности slug
                updated_category = self._repo.update(session, category_id, category_data)

                if not updated_category:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось обновить категорию"
                    )

                return Category.model_validate(updated_category)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении категории: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )