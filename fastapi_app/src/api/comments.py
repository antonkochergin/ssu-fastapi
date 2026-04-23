from fastapi import APIRouter, status
from fastapi_app.src.schemas.comments import Comment, CommentCreate, CommentUpdate
from fastapi_app.src.domain.comments_use_cases.get_comment import GetCommentUseCase
from fastapi_app.src.domain.comments_use_cases.create_comment import CreateCommentUseCase
from fastapi_app.src.domain.comments_use_cases.update_comment import UpdateCommentUseCase
from fastapi_app.src.domain.comments_use_cases.delete_comment import DeleteCommentUseCase
from fastapi_app.src.core.exeptions.exceptions import AppException
from .posts import handle_app_exception

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate) -> Comment:
    """Создать новый комментарий"""
    try:
        use_case = CreateCommentUseCase()
        return await use_case.execute(
            author_id=comment_data.author_id,
            post_id=comment_data.post_id,
            comment_data=comment_data
        )
    except AppException as e:
        return handle_app_exception(e)

@router.get("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def get_comment(comment_id: int) -> Comment:
    """Получить комментарий по ID"""
    try:
        use_case = GetCommentUseCase()
        return await use_case.execute(comment_id=comment_id)
    except AppException as e:
        return handle_app_exception(e)

@router.put("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def update_comment(comment_id: int, comment_data: CommentUpdate) -> Comment:
    """Обновить комментарий"""
    try:
        use_case = UpdateCommentUseCase()
        return await use_case.execute(
            comment_id=comment_id,
            comment_data=comment_data,
            user_id=1
        )
    except AppException as e:
        return handle_app_exception(e)

@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int) -> dict:
    """Удалить комментарий"""
    try:
        use_case = DeleteCommentUseCase()
        return await use_case.execute(
            comment_id=comment_id,
            user_id=1
        )
    except AppException as e:
        return handle_app_exception(e)