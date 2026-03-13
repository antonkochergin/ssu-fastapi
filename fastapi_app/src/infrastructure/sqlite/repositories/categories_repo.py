from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi_app.src.infrastructure.sqlite.models.categories import Category
from fastapi_app.src.schemas.categories import CategoryCreate, CategoryUpdate
from datetime import datetime

class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get_by_id(self, session: Session, category_id: int) -> Optional[Category]:
        return session.get(self.model, category_id)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        return session.query(self.model).offset(skip).limit(limit).all()

    def create(self, session: Session, category_data: CategoryCreate) -> Category:
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

    def update(self, session: Session, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        category = self.get_by_id(session, category_id)
        if not category:
            return None

        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(category, field) and value is not None:
                setattr(category, field, value)

        return category

    def delete(self, session: Session, category_id: int) -> bool:
        category = self.get_by_id(session, category_id)
        if category:
            session.delete(category)
            return True
        return False