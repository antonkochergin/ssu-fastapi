from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.comments_repo import CommentRepository
from fastapi_app.src.schemas.comments import CommentUpdate, Comment
from fastapi_app.src.exeptions import AppException, NotFoundException, DatabaseException

class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, user_id: int, comment_data: CommentUpdate) -> Comment:
        try:
            with self._database.session() as session:
                # 1. Проверяем существование
                existing_comment = self._repo.get_by_id(session, comment_id)
                if not existing_comment:
                    raise NotFoundException(resource="Комментарий", field="id", value=comment_id)

                # 2. Проверяем авторство (только автор может менять текст)
                if existing_comment.author_id != user_id:
                    raise AppException(
                        message="Вы не можете редактировать чужой комментарий",
                        code="forbidden"
                    )

                # 3. Обновляем
                updated_comment = self._repo.update(session, comment_id, comment_data)
                if not updated_comment:
                    raise DatabaseException(message="Не удалось сохранить изменения")

                return Comment.model_validate(updated_comment)
        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка при обновлении: {str(e)}")