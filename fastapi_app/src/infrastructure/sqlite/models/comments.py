from sqlalchemy import Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from fastapi_app.src.infrastructure.sqlite.database import Base


class Comment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_post.id"), nullable=False)

    def __repr__(self):
        return f"<Comment(id={self.id}, author_id={self.author_id}, post_id={self.post_id})>"