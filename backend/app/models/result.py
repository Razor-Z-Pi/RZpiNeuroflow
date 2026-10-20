from sqlalchemy import Integer, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ExerciseResult(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), unique=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)          # общий балл 0-100
    accuracy: Mapped[float] = mapped_column(Float, default=0.0)       # %
    speed_wpm: Mapped[int] = mapped_column(Integer, default=0)        # для чтения
    memory_items: Mapped[int] = mapped_column(Integer, default=0)     # для памяти
    errors: Mapped[int] = mapped_column(Integer, default=0)

    session = relationship("Session", back_populates="result")