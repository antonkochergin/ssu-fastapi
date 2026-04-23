from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_app.src.infrastructure.sqlite.models.locations import Location
from fastapi_app.src.schemas.locations import LocationCreate, LocationUpdate
from fastapi_app.src.core.exeptions.exceptions import QueryError
from datetime import datetime

class LocationRepository:
    def __init__(self):
        self.model = Location

    def get_by_name(self, session: Session, name: str) -> Optional[Location]:
        return session.query(self.model).filter(self.model.name == name).first()

    def get_by_id(self, session: Session, location_id: int) -> Optional[Location]:
        try:
            return session.get(self.model, location_id)
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_location")

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Location]:
        try:
            return session.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_location")

    def create(self, session: Session, location_data: LocationCreate) -> Location:
        try:
            location = self.model(
                name=location_data.name,
                is_published=location_data.is_published,
                created_at=datetime.now()
            )
            session.add(location)
            session.flush()
            return location
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_location")

    def update(self, session: Session, location_id: int, location_data: LocationUpdate) -> Optional[Location]:
        try:
            location = self.get_by_id(session, location_id)
            if not location:
                return None

            update_data = location_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(location, field) and value is not None:
                    setattr(location, field, value)
            session.flush()
            return location
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_location")

    def delete(self, session: Session, location_id: int) -> bool:
        try:
            location = self.get_by_id(session, location_id)
            if not location:
                return False
            session.delete(location)
            session.flush()
            return True
        except SQLAlchemyError as e:
            raise QueryError(message=str(e), table="blog_location")