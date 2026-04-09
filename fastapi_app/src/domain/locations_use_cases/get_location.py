from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.locations_repo import LocationRepository
from fastapi_app.src.schemas.locations import Location
from fastapi_app.src.exeptions import AppException, NotFoundException, DatabaseException

class GetLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(session, location_id)
                if not location:
                    raise NotFoundException(resource="Локация", field="id", value=location_id)
                return Location.model_validate(location)
        except AppException: raise
        except Exception as e:
            raise DatabaseException(message=str(e))