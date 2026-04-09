from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from fastapi_app.src.schemas.posts import PostUpdate, Post
from fastapi_app.src.exeptions import AppException, NotFoundException, UnprocessableError, DatabaseException

class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, post_data: PostUpdate, user_id: int, is_superuser: bool = False) -> Post:
        try:
            with self._database.session() as session:
                existing_post = self._repo.get_by_id(session, post_id)
                if not existing_post:
                    raise NotFoundException(resource="Пост", field="id", value=post_id)

                if existing_post.author_id != user_id and not is_superuser:
                    raise UnprocessableError(message="Вы можете редактировать только свои посты")

                updated_post = self._repo.update(session, post_id, post_data)
                if not updated_post:
                    raise DatabaseException(message="Не удалось обновить пост")

                return Post.model_validate(updated_post)

        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка обновления: {str(e)}")