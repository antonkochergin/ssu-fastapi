from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class LocationBase(BaseModel):
    """Базовая модель локации"""
    name: str = Field(...,min_length=3,  max_length=256)
    is_published: bool = Field(True)

class LocationCreate(LocationBase):
    """Для создания локации"""

class LocationUpdate(BaseModel):
    """Для обновления локации - все поля опциональны"""
    name: str | None = Field(None, min_length=3, max_length=256)
    is_published: bool | None = Field(None)

class Location(LocationBase):
    """Для чтения локации из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)