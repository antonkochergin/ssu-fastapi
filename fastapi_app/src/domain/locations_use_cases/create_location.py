from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.locations_repo import LocationRepository
from fastapi_app.src.schemas.locations import LocationCreate, Location


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> Location:
        try:
            with self._database.session() as session:
                new_location = self._repo.create(session, location_data)

                if not new_location:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось создать локацию"
                    )

                return Location.model_validate(new_location)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании локации: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )