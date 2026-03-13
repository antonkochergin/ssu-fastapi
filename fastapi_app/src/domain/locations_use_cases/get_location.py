from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.locations_repo import LocationRepository
from fastapi_app.src.schemas.locations import Location


class GetLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(session, location_id)

                if not location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с ID {location_id} не найдена"
                    )

                return Location.model_validate(location)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении локации: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )