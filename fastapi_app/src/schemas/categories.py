from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CategoryBase(BaseModel):
    """Базовая модель категории"""
    title: str = Field(..., min_length=3 , max_length=32)
    description: str = Field("", max_length=150)
    slug: str = Field(
        ...,
        max_length=32,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    is_published: bool = Field(True)


class CategoryCreate(CategoryBase):
    """Для создания категории - всё наследуется от базового класса"""

class CategoryUpdate(BaseModel):
    """Для обновления категории - все поля опциональны"""
    title: str|None = Field(None, min_length=3 ,max_length=32)
    description: str | None = Field(None, max_length=150)
    slug: str | None = Field(
        None,
        max_length=32,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    is_published: bool | None= Field(None)

class Category(CategoryBase):
    """Для чтения категории из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

