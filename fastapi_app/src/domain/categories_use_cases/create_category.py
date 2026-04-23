import re
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository
from fastapi_app.src.schemas.categories import CategoryCreate, Category
from fastapi_app.src.core.exeptions.exceptions import AppException, ConflictError, DatabaseException

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
                if self._repo.get_by_title(session, category_data.title):
                    raise ConflictError(
                        resource="Категория",
                        field="title",
                        value=category_data.title
                    )

                if not category_data.slug:
                    category_data.slug = self._generate_slug(category_data.title)

                if self._repo.get_by_slug(session, category_data.slug):
                    raise ConflictError(
                        resource="Категория",
                        field="slug",
                        value=category_data.slug
                    )

                new_category = self._repo.create(session, category_data)
                return Category.model_validate(new_category)

        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка создания категории: {str(e)}")