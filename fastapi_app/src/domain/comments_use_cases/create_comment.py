from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.comments_repo import CommentRepository
from fastapi_app.src.schemas.comments import CommentCreate, Comment
from fastapi_app.src.core.exeptions.exceptions import AppException, DatabaseException

class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, author_id: int, post_id: int, comment_data: CommentCreate) -> Comment:
        try:
            with self._database.session() as session:
                new_comment = self._repo.create(session, comment_data, post_id, author_id)
                return Comment.model_validate(new_comment)
        except AppException: raise
        except Exception as e:
            raise DatabaseException(message=f"Ошибка создания комментария: {str(e)}")