from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field, EmailStr

class UserBase(BaseModel):
    """Базовая модель пользователя - общие поля для всех схем"""
    username: str = Field(min_length=3, max_length=150)
    email: EmailStr | None = Field(None, max_length=254)
    first_name: str | None = Field(None, max_length=150)  # В модели max_length=128
    last_name: str | None = Field(None, max_length=150)   # В модели max_length=128
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    username: str = Field(..., min_length=3, max_length=150)
class UserUpdate(BaseModel):
    """Для обновления пользователя все поля необязательные"""
    username: str | None = Field(None, min_length=3, max_length=150)
    password: str | None = Field(None, min_length=8)
    email: EmailStr | None = Field(None, max_length=254)
    first_name: str | None = Field(None,max_length=150)
    last_name: str | None = Field(None,max_length=150)
    is_active: bool |None = None

class User(UserBase):
    """Для чтения пользователя из БД (без пароля) - полная модель"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_superuser: bool
    is_staff: bool
    date_joined: datetime
    last_login: datetime | None = None
    email: str | None = None  # Переопределяем, т.к. в БД это строка, а не EmailStr
