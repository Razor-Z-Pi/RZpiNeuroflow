from datetime import datetime
from pydantic import BaseModel, Field


class ExerciseResultIn(BaseModel):
    exercise_type: str = Field(pattern="^(reading|memory|attention|logic)$")
    duration_sec: int = Field(ge=1)
    accuracy: float = Field(ge=0, le=100)
    speed_wpm: int = Field(ge=0, default=0)
    memory_items: int = Field(ge=0, default=0)
    errors: int = Field(ge=0, default=0)


class AchievementShort(BaseModel):
    code: str
    title: str
    description: str
    icon: str


class ExerciseResultOut(BaseModel):
    id: int
    score: float
    accuracy: float
    speed_wpm: int
    memory_items: int
    errors: int
    created_at: datetime
    unlocked_achievements: list[AchievementShort] = []


class StatsResponse(BaseModel):
    avg_wpm: float
    avg_accuracy: float
    best_memory: int
    total_sessions: int
    streak_days: int
    history: list[dict]