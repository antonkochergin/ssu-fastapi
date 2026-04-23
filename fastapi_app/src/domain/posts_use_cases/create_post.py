import logging
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from fastapi_app.src.schemas.posts import PostCreate, Post
from fastapi_app.src.infrastructure.sqlite.models.categories import Category
from fastapi_app.src.infrastructure.sqlite.models.locations import Location
from fastapi_app.src.core.exeptions.exceptions import AppException, ValidationError, NotFoundException, DatabaseException

logger = logging.getLogger(__name__)

class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, author_id: int, post_data: PostCreate) -> Post:
        try:
            with self._database.session() as session:
                if not author_id:
                    raise ValidationError(message="ID автора обязателен", field="author_id")

                if post_data.category_id is not None:
                    category = session.get(Category, post_data.category_id)
                    if not category:
                        raise NotFoundException(resource="Category", field="id", value=post_data.category_id)

                if post_data.location_id is not None:
                    location = session.get(Location, post_data.location_id)
                    if not location:
                        raise NotFoundException(resource="Location", field="id", value=post_data.location_id)

                new_post = self._repo.create(session, post_data, author_id)
                if not new_post:
                    raise DatabaseException(message="Не удалось создать пост в базе данных")

                return Post.model_validate(new_post)

        except AppException:
            raise
        except Exception as e:
            logger.error(f"Ошибка при создании поста: {e}", exc_info=True)
            raise DatabaseException(message="Внутренняя ошибка сервера при создании записи")