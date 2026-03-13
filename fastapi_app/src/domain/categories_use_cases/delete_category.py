from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing_category = self._repo.get_by_id(session, category_id)
                if not existing_category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с ID {category_id} не найдена"
                    )

                deleted = self._repo.delete(session, category_id)

                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить категорию"
                    )

                return {"message": f"Категория с ID {category_id} успешно удалена"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении категории: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )