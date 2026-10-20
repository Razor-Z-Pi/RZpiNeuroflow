from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.session import Session
from app.models.result import ExerciseResult
from app.models.achievement import Achievement


# code -> (название, описание, условие)
ACHIEVEMENTS = {
    "first_session": {
        "title": "Первый шаг",
        "description": "Заверши первую тренировку",
        "icon": "check",
    },
    "streak_7": {
        "title": "Неделя силы",
        "description": "7 дней подряд без пропусков",
        "icon": "flame",
    },
    "streak_30": {
        "title": "Месяц дисциплины",
        "description": "30 дней подряд",
        "icon": "flame",
    },
    "wpm_100": {
        "title": "Сотня",
        "description": "Скорость чтения 100 wpm",
        "icon": "reading",
    },
    "wpm_200": {
        "title": "Двойная сотня",
        "description": "Скорость чтения 200 wpm",
        "icon": "reading",
    },
    "wpm_300": {
        "title": "Скорочтение",
        "description": "Скорость чтения 300 wpm",
        "icon": "reading",
    },
    "memory_10": {
        "title": "Полный порядок",
        "description": "10 из 10 слов в Дворце памяти",
        "icon": "memory",
    },
    "accuracy_90": {
        "title": "Снайпер",
        "description": "Точность 90% и выше",
        "icon": "attention",
    },
    "sessions_50": {
        "title": "Полсотни",
        "description": "50 тренировок всего",
        "icon": "chart",
    },
    "sessions_100": {
        "title": "Сотня сессий",
        "description": "100 тренировок всего",
        "icon": "chart",
    },
}


async def check_achievements(user: User, db: AsyncSession) -> list[Achievement]:
    """Проверяет и разблокирует достижения. Возвращает список новых."""
    unlocked = (await db.execute(
        select(Achievement.code).where(Achievement.user_id == user.id)
    )).scalars().all()
    unlocked_set = set(unlocked)

    # Считаем метрики
    total_sessions = (await db.execute(
        select(func.count(Session.id)).where(Session.user_id == user.id)
    )).scalar() or 0

    max_wpm = (await db.execute(
        select(func.max(ExerciseResult.speed_wpm))
        .join(Session, Session.id == ExerciseResult.session_id)
        .where(Session.user_id == user.id)
    )).scalar() or 0

    max_memory = (await db.execute(
        select(func.max(ExerciseResult.memory_items))
        .join(Session, Session.id == ExerciseResult.session_id)
        .where(Session.user_id == user.id)
    )).scalar() or 0

    max_accuracy = (await db.execute(
        select(func.max(ExerciseResult.accuracy))
        .join(Session, Session.id == ExerciseResult.session_id)
        .where(Session.user_id == user.id)
    )).scalar() or 0

    # streak
    rows = (await db.execute(
        select(Session.started_at).where(Session.user_id == user.id)
    )).scalars().all()
    days = {r.date() for r in rows}
    streak = 0
    from datetime import datetime as dt, timedelta
    cursor = dt.utcnow().date()
    while cursor in days:
        streak += 1
        cursor -= timedelta(days=1)

    # Определяем что разблокировать
    checks = {
        "first_session": total_sessions >= 1,
        "streak_7": streak >= 7,
        "streak_30": streak >= 30,
        "wpm_100": max_wpm >= 100,
        "wpm_200": max_wpm >= 200,
        "wpm_300": max_wpm >= 300,
        "memory_10": max_memory >= 10,
        "accuracy_90": max_accuracy >= 90,
        "sessions_50": total_sessions >= 50,
        "sessions_100": total_sessions >= 100,
    }

    new_achievements = []
    for code, passed in checks.items():
        if passed and code not in unlocked_set:
            a = Achievement(user_id=user.id, code=code)
            db.add(a)
            new_achievements.append(a)

    if new_achievements:
        await db.commit()
        for a in new_achievements:
            await db.refresh(a)

    return new_achievements