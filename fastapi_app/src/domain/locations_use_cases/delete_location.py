from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.locations_repo import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> dict:
        try:
            with self._database.session() as session:
                existing_location = self._repo.get_by_id(session, location_id)
                if not existing_location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с ID {location_id} не найдена"
                    )

                deleted = self._repo.delete(session, location_id)

                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось удалить локацию"
                    )

                return {"message": f"Локация с ID {location_id} успешно удалена"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении локации: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )