from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.comments_repo import CommentRepository
from fastapi_app.src.schemas.comments import Comment


class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Comment:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)

                if not comment:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с ID {comment_id} не найден"
                    )

                return Comment.model_validate(comment)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении комментария: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )