from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.comments_repo import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing_comment = self._repo.get_by_id(session, comment_id)
                if not existing_comment:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с ID {comment_id} не найден"
                    )

                deleted = self._repo.delete(session, comment_id)

                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить комментарий"
                    )

                return {"message": f"Комментарий с ID {comment_id} успешно удален"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении комментария: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )