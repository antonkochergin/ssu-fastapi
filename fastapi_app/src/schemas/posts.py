from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class PostBase(BaseModel):
    """Базовая модель поста - общие поля"""
    title: str = Field(..., min_length=3, max_length=256)
    text: str = Field(...)
    pub_date: datetime = Field(...)
    is_published: bool = Field(True)
    # Внешние ключи - часть сущности

    category_id: int | None = Field(None, gt=0)
    location_id: int | None = Field(None, gt=0)
    image: str | None = Field(None, min_length=3 ,max_length=100)


class PostCreate(PostBase):
    """Для создания поста - все поля базового класса"""

class PostUpdate(BaseModel):
    """Для обновления поста - все поля опциональны"""
    title: str | None = Field(None, min_length=3, max_length=256)
    text: str | None = Field(None)
    pub_date: datetime | None = Field(None)
    is_published: bool | None = Field(None)
    category_id: int | None = Field(None, gt=0)
    location_id: int | None = Field(None, gt=0)
    image: str | None = Field(None, min_length=3, max_length=100)


class Post(PostBase):
    """Для чтения поста из БД"""
    id: int
    created_at: datetime
    author_id: int

    model_config = ConfigDict(from_attributes=True)
