# fastapi_app/src/api/posts.py
from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from fastapi_app.src.schemas.posts import Post, PostCreate, PostUpdate
from fastapi_app.src.domain.posts_use_cases.create_post import CreatePostUseCase
from fastapi_app.src.domain.posts_use_cases.get_post import GetPostUseCase
from fastapi_app.src.domain.posts_use_cases.update_post import UpdatePostUseCase
from fastapi_app.src.domain.posts_use_cases.delete_post import DeletePostUseCase
from fastapi_app.src.exeptions import AppException
router = APIRouter(prefix="/posts", tags=["Posts"])

def handle_app_exception(exc: AppException) -> JSONResponse:
    """Конвертация AppException в HTTPException"""
    status_code_map = {
        "not_found": status.HTTP_404_NOT_FOUND,
        "conflict": status.HTTP_409_CONFLICT,
        "validation_error": status.HTTP_400_BAD_REQUEST,
        "unprocessable": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "database_error": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "db_connection_error": status.HTTP_503_SERVICE_UNAVAILABLE,
        "db_query_error": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "db_integrity_error": status.HTTP_400_BAD_REQUEST,
    }
    status_code = status_code_map.get(exc.code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate) -> Post:
    try:
        use_case = CreatePostUseCase()
        return await use_case.execute(author_id=1, post_data=post_data)
    except AppException as e:
        return handle_app_exception(e)

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int) -> Post:
    try:
        use_case = GetPostUseCase()
        return await use_case.execute(post_id=post_id)
    except AppException as e:
        return handle_app_exception(e)


@router.put("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_data: PostUpdate) -> Post:
    try:
        use_case = UpdatePostUseCase()
        return await use_case.execute(
            post_id=post_id,
            post_data=post_data,
            user_id=1
        )
    except AppException as e:
        return handle_app_exception(e)


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int) -> dict:
    """Удалить пост"""
    try:
        use_case = DeletePostUseCase()
        return await use_case.execute(
            post_id=post_id,
            user_id=1
        )
    except AppException as e:
        return handle_app_exception(e)
