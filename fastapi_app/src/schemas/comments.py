from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    """Базовая модель комментария"""
    text: str = Field(..., max_length=1000, description="Текст комментария")

class CommentCreate(BaseModel):
    """Для создания комментария"""
    text: str = Field(..., max_length=1000, description="Текст комментария")
    post_id: int = Field(..., description="ID поста")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Отличная статья!",
                "post_id": 42
            }
        }


class CommentUpdate(BaseModel):
    """Для обновления комментария"""
    text: Optional[str] = Field(None, max_length=1000, description="Текст комментария")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Обновленный текст комментария"
            }
        }


class Comment(BaseModel):
    """Для чтения комментария из БД"""
    id: int
    text: str
    author_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

