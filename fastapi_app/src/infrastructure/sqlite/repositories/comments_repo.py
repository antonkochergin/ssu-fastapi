from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_app.src.infrastructure.sqlite.models.comments import Comment
from fastapi_app.src.schemas.comments import CommentCreate, CommentUpdate
from fastapi_app.src.core.exeptions.exceptions import QueryError
from datetime import datetime

class CommentRepository:
    def __init__(self):
        self.model = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Optional[Comment]:
        try:
            return session.get(self.model, comment_id)
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_comment")

    def get_by_post(self, session: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        try:
            return session.query(self.model).filter(
                self.model.post_id == post_id
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_comment")

    def create(self, session: Session, comment_data: CommentCreate, post_id: int, author_id: int) -> Comment:
        try:
            comment = self.model(
                text=comment_data.text,
                post_id=post_id,
                author_id=author_id,
                created_at=datetime.now()
            )
            session.add(comment)
            session.flush()
            return comment
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_comment")

    def update(self, session: Session, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        comment = self.get_by_id(session, comment_id)
        if not comment:
            return None
        try:
            update_data = comment_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(comment, field) and value is not None:
                    setattr(comment, field, value)
            session.flush()
            return comment
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_comment")

    def delete(self, session: Session, comment_id: int) -> bool:
        comment = self.get_by_id(session, comment_id)
        if not comment:
            return False
        try:
            session.delete(comment)
            session.flush()
            return True
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_comment")