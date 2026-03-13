from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.posts_repo import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, user_id: int, is_superuser: bool = False) -> dict:
        try:
            with self._database.session() as session:
                existing_post = self._repo.get_by_id(session, post_id)
                if not existing_post:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с ID {post_id} не найден"
                    )

                if existing_post.author_id != user_id and not is_superuser:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Вы можете удалять только свои посты"
                    )

                deleted = self._repo.delete(session, post_id)

                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить пост"
                    )

                return {"message": f"Пост с ID {post_id} успешно удален"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении поста: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )