from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from fastapi_app.src.schemas.posts import Post
from fastapi_app.src.core.exeptions.exceptions import NotFoundException, DatabaseException # Импортируем свои

class GetPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> Post:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                if not post:
                    # Используем твой кастомный класс
                    raise NotFoundException(resource="Пост", field="id", value=post_id)
                return Post.model_validate(post)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка при получении поста: {str(e)}")