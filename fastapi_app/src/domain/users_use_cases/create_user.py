from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import UserCreate, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        try:
            with self._database.session() as session:
                # Проверка уникальности username
                existing_username = self._repo.get_by_username(session, user_data.username)
                if existing_username:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Пользователь с username '{user_data.username}' уже существует"
                    )

                # Проверка уникальности email (если указан)
                if user_data.email:
                    existing_email = session.query(self._repo.model).filter(
                        self._repo.model.email == user_data.email
                    ).first()
                    if existing_email:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с email '{user_data.email}' уже существует"
                        )

                # Хешируем пароль
                hashed_password = pwd_context.hash(user_data.password)

                # Создаем пользователя
                new_user = self._repo.create(session, user_data, hashed_password)

                if not new_user:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Не удалось создать пользователя"
                    )

                return User.model_validate(new_user)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )