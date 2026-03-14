from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    """Базовая модель комментария"""
    text: str = Field(..., min_length=1, max_length=1000)
    post_id: int = Field(..., gt=0)
    author_id: int = Field(..., gt=0)  # gt=0 <=> больше нуля


class CommentCreate(CommentBase):
    """Для создания комментария - все наследуется от базового класса"""


class CommentUpdate(BaseModel):
    """Для обновления комментария"""
    text: str | None = Field(None, min_length=1, max_length=1000)


class Comment(CommentBase):
    """Для чтения комментария из БД"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
