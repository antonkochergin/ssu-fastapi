from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from fastapi_app.src.schemas.posts import Post


class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> Post:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)

                if not post:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с ID {post_id} не найден"
                    )

                return Post.model_validate(post)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении поста: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )