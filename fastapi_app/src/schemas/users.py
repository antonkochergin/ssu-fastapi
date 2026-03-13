from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    """Базовая модель пользователя - общие поля для всех схем"""
    username: str = Field(min_length=3, max_length=150)
    email: str | None = Field(None, max_length=254)
    first_name: str | None = Field(None, max_length=128)  # В модели max_length=128
    last_name: str | None = Field(None, max_length=128)   # В модели max_length=128
    is_active: bool = True


class UserCreate(BaseModel):
    """Для создания пользователя - все поля необязательные кроме username и password"""
    username: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=8, max_length=128)  # Добавил max_length как в модели
    email: EmailStr | None = None
    first_name: str | None = Field(None, max_length=128)
    last_name: str | None = Field(None, max_length=128)
    is_active: bool = True

    is_staff: bool = False
    is_superuser: bool = False


class UserUpdate(BaseModel):
    """Для обновления пользователя все поля необязательные"""
    username: str | None = Field(None, min_length=3, max_length=150)
    password: str | None = Field(None, min_length=8, max_length=128)
    email: EmailStr | None = None
    first_name: str | None = Field(None, max_length=128)
    last_name: str | None = Field(None, max_length=128)
    is_active: bool | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None


class User(UserBase):
    """Для чтения пользователя из БД (без пароля) - полная модель"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_superuser: bool
    is_staff: bool
    date_joined: datetime
    last_login: datetime | None = None
    email: str | None = None  # Переопределяем, т.к. в БД это строка, а не EmailStr
