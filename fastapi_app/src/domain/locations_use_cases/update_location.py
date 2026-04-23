from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.locations_repo import LocationRepository
from fastapi_app.src.schemas.locations import LocationUpdate, Location
from fastapi_app.src.core.exeptions.exceptions import AppException, NotFoundException, DatabaseException

class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, location_data: LocationUpdate) -> Location:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, location_id)
                if not existing:
                    raise NotFoundException(resource="Локация", field="id", value=location_id)

                updated = self._repo.update(session, location_id, location_data)
                return Location.model_validate(updated)
        except AppException: raise
        except Exception as e:
            raise DatabaseException(message=str(e))