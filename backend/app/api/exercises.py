from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.session import Session
from app.models.result import ExerciseResult
from app.schemas.exercise import ExerciseResultIn, ExerciseResultOut
from app.services.achievements import check_achievements, ACHIEVEMENTS

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


@router.post("/submit", response_model=ExerciseResultOut)
async def submit(
    data: ExerciseResultIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # расчёт интегрального балла
    score = data.accuracy * 0.6
    if data.exercise_type == "reading":
        score += min(data.speed_wpm / 400, 1.0) * 40
    elif data.exercise_type == "memory":
        score += min(data.memory_items / 20, 1.0) * 40
    elif data.exercise_type == "attention":
        score += max(0.0, (100 - data.errors) / 100) * 40
    else:
        score += 40 * (1 - min(data.errors, 10) / 10)

    session = Session(
        user_id=current_user.id,
        exercise_type=data.exercise_type,
        duration_sec=data.duration_sec,
    )
    db.add(session)
    await db.flush()

    result = ExerciseResult(
        session_id=session.id,
        score=round(score, 2),
        accuracy=data.accuracy,
        speed_wpm=data.speed_wpm,
        memory_items=data.memory_items,
        errors=data.errors,
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)

    new_achievements = await check_achievements(current_user, db)
    unlocked = [
        {"code": a.code, **ACHIEVEMENTS[a.code]} for a in new_achievements
    ]

    return ExerciseResultOut(
        id=result.id,
        score=result.score,
        accuracy=result.accuracy,
        speed_wpm=result.speed_wpm,
        memory_items=result.memory_items,
        errors=result.errors,
        created_at=session.started_at,
        unlocked_achievements=unlocked,
    )