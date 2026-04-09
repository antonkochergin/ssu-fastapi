from fastapi import APIRouter, status
from fastapi_app.src.schemas.users import User, UserCreate, UserUpdate
from fastapi_app.src.domain.users_use_cases.create_user import CreateUserUseCase
from fastapi_app.src.domain.users_use_cases.get_user import GetUserUseCase
from fastapi_app.src.domain.users_use_cases.get_user_by_username import GetUserByUsernameUseCase
from fastapi_app.src.domain.users_use_cases.get_all_users import GetAllUsersUseCase
from fastapi_app.src.domain.users_use_cases.update_user import UpdateUserUseCase
from fastapi_app.src.domain.users_use_cases.delete_user import DeleteUserUseCase
from fastapi_app.src.exeptions import AppException
from .posts import handle_app_exception

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """Создать нового пользователя"""
    try:
        return await CreateUserUseCase().execute(user_data)
    except AppException as e:
        return handle_app_exception(e)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Получить пользователя по ID"""
    try:
        return await GetUserUseCase().execute(user_id)
    except AppException as e:
        return handle_app_exception(e)

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