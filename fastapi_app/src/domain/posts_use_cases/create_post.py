from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from fastapi_app.src.schemas.posts import PostCreate, Post


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, author_id: int, post_data: PostCreate) -> Post:
        try:
            with self._database.session() as session:
                new_post = self._repo.create(session, post_data, author_id)

                if not new_post:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось создать пост"
                    )

                return Post.model_validate(new_post)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании поста: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )