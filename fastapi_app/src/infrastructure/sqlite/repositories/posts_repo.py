# src/infrastructure/sqlite/repositories/post.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi_app.src.infrastructure.sqlite.models.posts import Post
from fastapi_app.src.schemas.posts import PostCreate, PostUpdate
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi_app.src.exeptions import QueryError, IntegrityError

class PostRepository:
    def __init__(self):
        self.model = Post

    def get_by_id(self, session: Session, post_id: int) -> Optional[Post]:
        try:
            return session.get(self.model, post_id)
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="posts")

    def create(self, session: Session, post_data: PostCreate, author_id: int) -> Post:
        try:
            post = self.model(
                title=post_data.title,
                text=post_data.text,
                pub_date=post_data.pub_date,
                is_published=post_data.is_published,
                author_id=author_id,
                category_id=post_data.category_id,
                location_id=post_data.location_id,
                image=post_data.image,
                created_at=datetime.now()
            )
            session.add(post)
            session.flush()
            return post
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="posts")

    def update(self, session: Session, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        post = self.get_by_id(session, post_id)
        if not post:
            return None

        update_data = post_data.model_dump(exclude_unset=True)
        forbidden_fields = ['id', 'created_at', 'author_id']

        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(post, field) and value is not None:
                setattr(post, field, value)

        return post

    def delete(self, session: Session, post_id: int) -> bool:
        post = self.get_by_id(session, post_id)
        if post:
            session.delete(post)
            return True
        return False