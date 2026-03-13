from fastapi_app.src.infrastructure.sqlite.database import Base
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Post(Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    pub_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"), nullable=False)
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("blog_category.id"), nullable=True)
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("blog_location.id"), nullable=True)
    image: Mapped[str | None] = mapped_column(String(100), nullable=True)

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"