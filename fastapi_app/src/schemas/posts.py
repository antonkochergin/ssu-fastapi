from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    """Базовая модель поста - общие поля"""
    title: str = Field(..., max_length=256, description="Заголовок")
    text: str = Field(..., description="Текст поста")
    pub_date: datetime = Field(..., description="Дата публикации")
    is_published: bool = Field(True, description="Опубликовано")
    # Внешние ключи - часть сущности
    author_id: int = Field(..., description="ID автора")
    category_id: Optional[int] = Field(None, description="ID категории")
    location_id: Optional[int] = Field(None, description="ID локации")
    image: Optional[str] = Field(None, max_length=100, description="URL изображения")


class PostCreate(BaseModel):
    """Для создания поста - все поля кроме author_id (берется из контекста)"""
    title: str = Field(..., max_length=256, description="Заголовок")
    text: str = Field(..., description="Текст поста")
    pub_date: datetime = Field(..., description="Дата публикации")
    is_published: bool = Field(True, description="Опубликовано")
    category_id: Optional[int] = Field(None, description="ID категории")
    location_id: Optional[int] = Field(None, description="ID локации")
    image: Optional[str] = Field(None, max_length=100, description="URL изображения")

class PostUpdate(BaseModel):
    """Для обновления поста - все поля опциональны"""
    title: Optional[str] = Field(None, max_length=256, description="Заголовок")
    text: Optional[str] = Field(None, description="Текст поста")
    pub_date: Optional[datetime] = Field(None, description="Дата публикации")
    is_published: Optional[bool] = Field(None, description="Опубликовано")
    category_id: Optional[int] = Field(None, description="ID категории")
    location_id: Optional[int] = Field(None, description="ID локации")
    image: Optional[str] = Field(None, max_length=100, description="URL изображения")

class Post(PostBase):
    """Для чтения поста из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
