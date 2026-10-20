from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.session import Session
from app.models.result import ExerciseResult
from app.schemas.exercise import StatsResponse
from app.models.achievement import Achievement
from app.services.achievements import ACHIEVEMENTS

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/me", response_model=StatsResponse)
async def my_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    q = (
        select(Session, ExerciseResult)
        .join(ExerciseResult, ExerciseResult.session_id == Session.id)
        .where(Session.user_id == current_user.id)
        .order_by(Session.started_at.asc())
    )
    rows = (await db.execute(q)).all()

    history = [
        {
            "date": s.started_at.isoformat(),
            "type": s.exercise_type,
            "score": r.score,
            "wpm": r.speed_wpm,
            "accuracy": r.accuracy,
            "memory": r.memory_items,
        }
        for s, r in rows
    ]

    avg_wpm = sum(r.speed_wpm for _, r in rows) / len(rows) if rows else 0.0
    avg_acc = sum(r.accuracy for _, r in rows) / len(rows) if rows else 0.0
    best_mem = max((r.memory_items for _, r in rows), default=0)

    # streak (дни подряд)
    days = {s.started_at.date() for s, _ in rows}
    streak = 0
    cursor = datetime.utcnow().date()
    while cursor in days:
        streak += 1
        cursor -= timedelta(days=1)

    return StatsResponse(
        avg_wpm=round(avg_wpm, 1),
        avg_accuracy=round(avg_acc, 1),
        best_memory=best_mem,
        total_sessions=len(rows),
        streak_days=streak,
        history=history,
    )

import csv
import io
from fastapi.responses import StreamingResponse


@router.get("/export/csv")
async def export_csv(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    q = (
        select(Session, ExerciseResult)
        .join(ExerciseResult, ExerciseResult.session_id == Session.id)
        .where(Session.user_id == current_user.id)
        .order_by(Session.started_at.asc())
    )
    rows = (await db.execute(q)).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "date", "exercise_type", "duration_sec",
        "score", "accuracy", "speed_wpm", "memory_items", "errors",
    ])
    for s, r in rows:
        writer.writerow([
            s.started_at.isoformat(),
            s.exercise_type,
            s.duration_sec,
            r.score,
            r.accuracy,
            r.speed_wpm,
            r.memory_items,
            r.errors,
        ])
    buffer.seek(0)

    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="neuroflow_{current_user.username}.csv"'
        },
    )

@router.get("/recommendation")
async def recommendation(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    q = (
        select(Session.exercise_type, func.avg(ExerciseResult.score))
        .join(ExerciseResult, ExerciseResult.session_id == Session.id)
        .where(Session.user_id == current_user.id)
        .group_by(Session.exercise_type)
    )
    rows = (await db.execute(q)).all()
    scores = {t: float(s) for t, s in rows}

    all_types = ["reading", "memory", "attention", "logic"]
    # Если какой-то тип ещё не тренировался — предлагаем его первым
    untrained = [t for t in all_types if t not in scores]
    if untrained:
        return {"recommended_type": untrained[0], "reason": "not_trained"}

    weakest = min(scores, key=scores.get)
    return {
        "recommended_type": weakest,
        "reason": "weakest",
        "avg_score": round(scores[weakest], 1),
    }

@router.get("/achievements")
async def my_achievements(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = (await db.execute(
        select(Achievement)
        .where(Achievement.user_id == current_user.id)
        .order_by(Achievement.unlocked_at.asc())
    )).scalars().all()

    unlocked_codes = {a.code for a in rows}

    result = []
    for code, meta in ACHIEVEMENTS.items():
        result.append({
            "code": code,
            **meta,
            "unlocked": code in unlocked_codes,
            "unlocked_at": next(
                (a.unlocked_at.isoformat() for a in rows if a.code == code),
                None,
            ),
        })
    return result