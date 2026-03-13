from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class LocationBase(BaseModel):
    """Базовая модель локации"""
    name: str = Field(..., max_length=256, description="Название локации")
    is_published: bool = Field(True, description="Опубликовано")


class LocationCreate(LocationBase):
    """Для создания локации"""
    pass


class LocationUpdate(BaseModel):
    """Для обновления локации - все поля опциональны"""
    name: Optional[str] = Field(None, max_length=256, description="Название локации")
    is_published: Optional[bool] = Field(None, description="Опубликовано")


class Location(LocationBase):
    """Для чтения локации из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

