from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import ValidationError

from fastapi_app.src.schemas.users import User, UserCreate, UserUpdate
from .src.domain.users.use_cases.get_users import GetUsersUseCase
from .src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase
from .src.domain.users.use_cases.get_user_by_username import GetUserByUsernameUseCase
from .src.domain.users.use_cases.get_user_by_login import GetUserByLoginUseCase
from .src.domain.users.use_cases.create_user import CreateUserUseCase
from .src.domain.users.use_cases.update_user import UpdateUserUseCase
from .src.domain.users.use_cases.delete_user import DeleteUserUseCase
from fastapi_app.src.api.depends import (
    get_get_user_by_login_use_case,
    create_user_use_case,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    UserUsernameIsNotUniqueException,
    UserEmailIsNotUniqueException,
)
from src.services.auth import AuthService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """Создать нового пользователя"""
    try:
        return await CreateUserUseCase().execute(user_data)
    except AppException as e:
        return handle_app_exception(e)

@router.get(
    "/by-login/{login}",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def get_user_by_login(
    login: str,
    user: User = Depends(AuthService.get_current_user),
    use_case: GetUserByLoginUseCase = Depends(get_get_user_by_login_use_case),
) -> User:
    try:
        return await use_case.execute(login=login)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())

@router.get("/username/{username}", response_model=User)
async def get_user_by_username(username: str):
    """Получить пользователя по username"""
    try:
        return await GetUserByUsernameUseCase().execute(username)
    except AppException as e:
        return handle_app_exception(e)

@router.get("/", response_model=list[User])
async def get_all_users(skip: int = 0, limit: int = 100):
    """Получить список всех пользователей"""
    try:
        return await GetAllUsersUseCase().execute(skip, limit)
    except AppException as e:
        return handle_app_exception(e)

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate):
    """Обновить данные пользователя"""
    try:
        return await UpdateUserUseCase().execute(user_id, user_data)
    except AppException as e:
        return handle_app_exception(e)

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Удалить пользователя"""
    try:
        return await DeleteUserUseCase().execute(user_id)
    except AppException as e:
        return handle_app_exception(e)