from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi_app.src.infrastructure.sqlite.models.comments import Comment
from fastapi_app.src.schemas.comments import CommentCreate, CommentUpdate
from datetime import datetime

class CommentRepository:
    def __init__(self):
        self.model = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Optional[Comment]:
        return session.get(self.model, comment_id)

    def get_by_post(self, session: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        return session.query(self.model).filter(
            self.model.post_id == post_id
        ).offset(skip).limit(limit).all()

    def create(self, session: Session, comment_data: CommentCreate, post_id: int, author_id: int) -> Comment:
        comment = self.model(
            text=comment_data.text,
            post_id=post_id,
            author_id=author_id,
            created_at=datetime.now()
        )
        session.add(comment)
        session.flush()
        return comment

    def update(self, session: Session, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        comment = self.get_by_id(session, comment_id)
        if not comment:
            return None

        update_data = comment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(comment, field) and value is not None:
                setattr(comment, field, value)

        return comment

    def delete(self, session: Session, comment_id: int) -> bool:
        comment = self.get_by_id(session, comment_id)
        if comment:
            session.delete(comment)
            return True
        return False