from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    exercise_type: Mapped[str] = mapped_column(String(64))  # reading | memory | attention | logic
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    duration_sec: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="sessions")
    result = relationship("ExerciseResult", back_populates="session", uselist=False, cascade="all, delete-orphan")