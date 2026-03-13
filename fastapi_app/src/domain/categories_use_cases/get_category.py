from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository
from fastapi_app.src.schemas.categories import Category


class GetCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Category:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)

                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с ID {category_id} не найдена"
                    )

                return Category.model_validate(category)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении категории: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )