from fastapi import APIRouter, status
from fastapi_app.src.schemas.categories import Category, CategoryCreate, CategoryUpdate
from fastapi_app.src.domain.categories_use_cases.create_category import CreateCategoryUseCase
from fastapi_app.src.domain.categories_use_cases.get_category import GetCategoryUseCase
from fastapi_app.src.domain.categories_use_cases.update_category import UpdateCategoryUseCase
from fastapi_app.src.domain.categories_use_cases.delete_category import DeleteCategoryUseCase
from fastapi_app.src.core.exeptions.exceptions import AppException
from .posts import handle_app_exception

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate) -> Category:
    """Создать новую категорию"""
    try:
        return await CreateCategoryUseCase().execute(category_data)
    except AppException as e:
        return handle_app_exception(e)

@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: int) -> Category:
    """Получить категорию по ID"""
    try:
        return await GetCategoryUseCase().execute(category_id)
    except AppException as e:
        return handle_app_exception(e)

@router.put("/{category_id}", response_model=Category)
async def update_category(category_id: int, category_data: CategoryUpdate) -> Category:
    """Обновить категорию"""
    try:
        return await UpdateCategoryUseCase().execute(category_id, category_data)
    except AppException as e:
        return handle_app_exception(e)

@router.delete("/{category_id}")
async def delete_category(category_id: int):
    """Удалить категорию"""
    try:
        return await DeleteCategoryUseCase().execute(category_id)
    except AppException as e:
        return handle_app_exception(e)