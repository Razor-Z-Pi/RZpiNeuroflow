from datetime import datetime
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # baseline (входной тест)
    baseline_wpm: Mapped[int] = mapped_column(Integer, default=0)
    baseline_comprehension: Mapped[int] = mapped_column(Integer, default=0)
    baseline_memory: Mapped[int] = mapped_column(Integer, default=0)

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")