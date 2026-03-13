from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.locations_repo import LocationRepository
from fastapi_app.src.schemas.locations import LocationUpdate, Location


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, location_data: LocationUpdate) -> Location:
        try:
            with self._database.session() as session:
                existing_location = self._repo.get_by_id(session, location_id)
                if not existing_location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с ID {location_id} не найдена"
                    )

                updated_location = self._repo.update(session, location_id, location_data)

                if not updated_location:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось обновить локацию"
                    )

                return Location.model_validate(updated_location)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении локации: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )