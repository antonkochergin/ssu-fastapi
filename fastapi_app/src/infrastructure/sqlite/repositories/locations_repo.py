from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi_app.src.infrastructure.sqlite.models.locations import Location
from fastapi_app.src.schemas.locations import LocationCreate, LocationUpdate
from datetime import datetime

class LocationRepository:
    def __init__(self):
        self.model = Location

    def get_by_id(self, session: Session, location_id: int) -> Optional[Location]:
        return session.get(self.model, location_id)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[Location]:
        return session.query(self.model).offset(skip).limit(limit).all()

    def create(self, session: Session, location_data: LocationCreate) -> Location:
        location = self.model(
            name=location_data.name,
            is_published=location_data.is_published,
            created_at=datetime.now()
        )
        session.add(location)
        session.flush()
        return location

    def update(self, session: Session, location_id: int, location_data: LocationUpdate) -> Optional[Location]:
        location = self.get_by_id(session, location_id)
        if not location:
            return None

        update_data = location_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(location, field) and value is not None:
                setattr(location, field, value)

        return location

    def delete(self, session: Session, location_id: int) -> bool:
        location = self.get_by_id(session, location_id)
        if location:
            session.delete(location)
            return True
        return False