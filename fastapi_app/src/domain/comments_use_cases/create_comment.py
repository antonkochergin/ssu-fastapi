from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.comments_repo import CommentRepository
from fastapi_app.src.schemas.comments import CommentCreate, Comment


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_data: CommentCreate) -> Comment:
        try:
            with self._database.session() as session:
                new_comment = self._repo.create(session, comment_data)

                if not new_comment:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось создать комментарий"
                    )

                return Comment.model_validate(new_comment)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании комментария: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )