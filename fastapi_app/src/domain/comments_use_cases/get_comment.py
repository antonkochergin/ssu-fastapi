from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.comments_repo import CommentRepository
from fastapi_app.src.schemas.comments import Comment
from fastapi_app.src.exeptions import AppException, NotFoundException, DatabaseException


class GetCommentUseCase:  # Убрали "ByPost", теперь это поиск одного объекта
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Comment:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)

                if not comment:
                    raise NotFoundException(
                        resource="Комментарий",
                        field="id",
                        value=comment_id
                    )

                return Comment.model_validate(comment)
        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка при получении комментария: {str(e)}")