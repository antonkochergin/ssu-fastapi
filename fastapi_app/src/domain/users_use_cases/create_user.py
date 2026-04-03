from fastapi import HTTPException, status
from fastapi_app.src.infrastructure.sqlite.database import database
from fastapi_app.src.infrastructure.sqlite.repositories.users_repo import UserRepository
from fastapi_app.src.schemas.users import UserCreate, User
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
import logging

logger = logging.getLogger(__name__)
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

        except IntegrityError as e:
            logger.error(f"Ошибка целостности данных при создании пользователя: {e}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Нарушение уникальности данных. Возможно, пользователь с таким username или email уже существует."
            )

        except OperationalError as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис временно недоступен. Ошибка подключения к базе данных."
            )

        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при создании пользователя: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка базы данных. Пожалуйста, попробуйте позже."
            )

        except Exception as e:
            logger.error(f"Неожиданная ошибка при создании пользователя: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
            )