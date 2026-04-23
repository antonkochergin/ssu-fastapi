from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_app.src.infrastructure.sqlite.models.categories import Category
from fastapi_app.src.schemas.categories import CategoryCreate, CategoryUpdate
from fastapi_app.src.core.exeptions.exceptions import QueryError
from datetime import datetime

class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get_by_id(self, session: Session, category_id: int) -> Optional[Category]:
        try:
            return session.get(self.model, category_id)
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_category")

    def get_by_title(self, session: Session, title: str) -> Optional[Category]:
        try:
            return session.query(self.model).filter(self.model.title == title).first()
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_category")

    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        try:
            return session.query(self.model).filter(self.model.slug == slug).first()
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_category")

    def create(self, session: Session, category_data: CategoryCreate) -> Category:
        try:
            category = self.model(
                title=category_data.title,
                slug=category_data.slug,
                description=category_data.description or "",
                is_published=category_data.is_published,
                created_at=datetime.now()
            )
            session.add(category)
            session.flush()
            return category
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_category")

    def update(self, session: Session, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        category = self.get_by_id(session, category_id)
        if not category:
            return None
        try:
            update_data = category_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(category, field) and value is not None:
                    setattr(category, field, value)
            session.flush()
            return category
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_category")

    def delete(self, session: Session, category_id: int) -> bool:
        category = self.get_by_id(session, category_id)
        if not category:
            return False
        try:
            session.delete(category)
            session.flush()
            return True
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_category")