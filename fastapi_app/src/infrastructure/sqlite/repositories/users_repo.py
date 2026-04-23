from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_app.src.infrastructure.sqlite.models.users import User
from fastapi_app.src.schemas.users import UserCreate, UserUpdate
from fastapi_app.src.core.exeptions.exceptions import QueryError
from datetime import datetime, timezone

class UserRepository:
    def __init__(self):
        self.model = User

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        try:
            return session.get(self.model, user_id)
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="auth_user")

    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        try:
            return session.query(self.model).filter(self.model.username == username).first()
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="auth_user")

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[User]:
        try:
            return session.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="auth_user")

    def create(self, session: Session, user_data: UserCreate, hashed_password: str) -> User:
        try:
            db_user = self.model(
                username=user_data.username,
                email=user_data.email,
                password=hashed_password,
                date_joined=datetime.now(timezone.utc),
                created_at=datetime.now(timezone.utc)
            )
            session.add(db_user)
            session.flush()
            return db_user
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="auth_user")

    def update(self, session: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get_by_id(session, user_id)
        if not user:
            return None
        try:
            update_data = user_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(user, field) and value is not None:
                    setattr(user, field, value)
            session.flush()
            return user
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="auth_user")

    def delete(self, session: Session, user_id: int) -> bool:
        user = self.get_by_id(session, user_id)
        if not user:
            return False
        try:
            session.delete(user)
            session.flush()
            return True
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="auth_user")