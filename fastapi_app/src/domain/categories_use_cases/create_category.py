from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository
from fastapi_app.src.schemas.categories import CategoryCreate, Category
import re


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    def _generate_slug(self, title: str) -> str:
        slug = title.lower().replace(' ', '-')
        slug = re.sub(r'[^a-zA-Z0-9-]', '', slug)
        return slug[:32]

    async def execute(self, category_data: CategoryCreate) -> Category:
        try:
            with self._database.session() as session:
                if not category_data.slug:
                    category_data.slug = self._generate_slug(category_data.title)

                existing = self._repo.get_by_slug(session, category_data.slug)
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Категория со slug '{category_data.slug}' уже существует"
                    )

                new_category = self._repo.create(session, category_data)

                if not new_category:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось создать категорию"
                    )

                return Category.model_validate(new_category)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании категории: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )