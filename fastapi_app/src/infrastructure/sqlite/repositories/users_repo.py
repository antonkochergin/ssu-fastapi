# src/infrastructure/sqlite/repositories/user.py
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi_app.src.infrastructure.sqlite.models.users import User
from fastapi_app.src.schemas.users import UserCreate, UserUpdate
from datetime import datetime

class UserRepository:
    def __init__(self):
        self.model = User

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        return session.get(self.model, user_id)

    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        return session.query(self.model).filter(self.model.username == username).first()

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return session.query(self.model).offset(skip).limit(limit).all()

    def create(self, session: Session, user_data: UserCreate, hashed_password: str) -> User:
        user = self.model(
            username=user_data.username,
            email=user_data.email or "",
            password=hashed_password,
            first_name=user_data.first_name or "",
            last_name=user_data.last_name or "",
            is_active=user_data.is_active,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
            last_login=None
        )
        session.add(user)
        session.flush()
        return user

    def update(self, session: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get_by_id(session, user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        forbidden_fields = ['id', 'date_joined']

        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(user, field) and value is not None:
                setattr(user, field, value)

        return user

    def delete(self, session: Session, user_id: int) -> bool:
        user = self.get_by_id(session, user_id)
        if user:
            session.delete(user)
            return True
        return False