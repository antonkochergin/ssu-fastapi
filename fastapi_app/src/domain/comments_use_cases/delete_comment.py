from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.comments_repo import CommentRepository
from fastapi_app.src.exeptions import AppException, NotFoundException, DatabaseException


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, user_id: int, is_superuser: bool = False) -> dict:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)
                if not comment:
                    raise NotFoundException(resource="Комментарий", field="id", value=comment_id)

                # Проверка прав (автор или админ)
                if comment.author_id != user_id and not is_superuser:
                    raise AppException(message="Нет прав на удаление этого комментария", code="forbidden")

                self._repo.delete(session, comment_id)
                return {"message": "Комментарий удален"}
        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=str(e))