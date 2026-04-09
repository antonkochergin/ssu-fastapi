from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.locations_repo import LocationRepository
from fastapi_app.src.exeptions import AppException, NotFoundException, DatabaseException

class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, location_id)
                if not existing:
                    raise NotFoundException(resource="Локация", field="id", value=location_id)

                self._repo.delete(session, location_id)
                return {"message": f"Локация с ID {location_id} успешно удалена"}
        except AppException: raise
        except Exception as e:
            raise DatabaseException(message=str(e))