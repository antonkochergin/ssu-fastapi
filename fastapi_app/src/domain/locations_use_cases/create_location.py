from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.locations_repo import LocationRepository
from fastapi_app.src.schemas.locations import LocationCreate, Location
from fastapi_app.src.core.exeptions.exceptions import AppException, DatabaseException, ConflictError


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> Location:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_name(session, location_data.name)
                if existing:
                    raise ConflictError(
                        resource="Локация",
                        field="name",
                        value=location_data.name
                    )

                new_location = self._repo.create(session, location_data)
                return Location.model_validate(new_location)

        except AppException:
            raise
        except Exception as e:
            raise DatabaseException(message=str(e))