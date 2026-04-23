from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from fastapi_app.src.core.exeptions.exceptions import AppException, NotFoundException, UnprocessableError, DatabaseException

class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, user_id: int, is_superuser: bool = False) -> dict:
        try:
            with self._database.session() as session:
                existing_post = self._repo.get_by_id(session, post_id)
                if not existing_post:
                    raise NotFoundException(resource="Пост", field="id", value=post_id)

                if existing_post.author_id != user_id and not is_superuser:
                    raise UnprocessableError(message="Вы можете удалять только свои посты")

                deleted = self._repo.delete(session, post_id)
                if not deleted:
                    raise DatabaseException(message="Не удалось удалить пост из БД")

                return {"message": f"Пост с ID {post_id} успешно удален"}

        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка удаления: {str(e)}")