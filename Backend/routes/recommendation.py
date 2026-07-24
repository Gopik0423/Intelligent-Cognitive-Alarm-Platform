from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.db import SessionLocal
from models.analytics import Analytics
from models.sleep import Sleep
from models.verification import WakeupVerification
from models.performance import Performance
from models.habit import Habit

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sleep_recommendations(user_id: int, db: Session) -> list[str]:
    sleep = db.query(Sleep).filter(Sleep.user_id == user_id).first()

    if not sleep:
        return ["No sleep schedule found. Add one to get sleep recommendations."]

    sleep_dt = datetime.combine(datetime.today(), sleep.sleep_time)
    wake_dt = datetime.combine(datetime.today(), sleep.wake_time)

    if wake_dt <= sleep_dt:
        wake_dt += timedelta(days=1)

    duration_hours = (wake_dt - sleep_dt).total_seconds() / 3600

    tips = []
    if duration_hours < 6:
        tips.append(f"You're only getting about {duration_hours:.1f} hours of sleep. Try going to bed earlier.")
    elif duration_hours > 9:
        tips.append(f"You're sleeping about {duration_hours:.1f} hours, which is longer than typical. Consider a more consistent schedule.")
    else:
        tips.append(f"Your sleep duration (~{duration_hours:.1f} hours) looks healthy. Keep it up!")

    return tips


def get_wakeup_recommendations(user_id: int, db: Session) -> list[str]:
    verifications = (
        db.query(WakeupVerification)
        .filter(WakeupVerification.user_id == user_id)
        .order_by(WakeupVerification.started_at.desc())
        .limit(10)
        .all()
    )

    tips = []

    if verifications:
        total = len(verifications)
        failed = sum(1 for v in verifications if v.status == "failed")
        fail_rate = failed / total

        if fail_rate > 0.4:
            tips.append("You're failing wake-up verification often. Try an easier challenge type in your alarm settings.")
        elif fail_rate == 0:
            tips.append("Great job — you're passing wake-up verification consistently!")

    recent_analytics = (
        db.query(Analytics)
        .filter(Analytics.user_id == user_id)
        .order_by(Analytics.id.desc())
        .limit(5)
        .all()
    )

    if recent_analytics:
        avg_snooze = sum(a.snooze_count or 0 for a in recent_analytics) / len(recent_analytics)
        if avg_snooze >= 3:
            tips.append(f"You're snoozing an average of {avg_snooze:.1f} times recently. Try setting your alarm earlier or using a harder wake-up challenge.")

    if not tips:
        tips.append("Not enough wake-up data yet to give a recommendation.")

    return tips


def get_productivity_recommendations(user_id: int, db: Session) -> list[str]:
    records = (
        db.query(Performance)
        .filter(Performance.user_id == user_id)
        .order_by(Performance.completed_at.desc())
        .limit(10)
        .all()
    )

    if not records:
        return ["Not enough puzzle performance data yet to give productivity tips."]

    avg_accuracy = sum(r.accuracy for r in records) / len(records)
    avg_completion_time = sum(r.completion_time for r in records) / len(records)

    tips = []

    if avg_accuracy < 0.5:
        tips.append(f"Your recent puzzle accuracy is around {avg_accuracy*100:.0f}%. Try easier challenges to build consistency first.")
    elif avg_accuracy >= 0.85:
        tips.append(f"Strong accuracy ({avg_accuracy*100:.0f}%)! Consider increasing challenge difficulty to stay engaged.")

    if avg_completion_time > 30:
        tips.append(f"You're taking about {avg_completion_time:.0f} seconds per challenge on average. A brisker morning routine may boost your daily productivity.")

    if not tips:
        tips.append("Your challenge performance looks balanced. Keep up your current routine.")

    return tips


def get_habit_recommendations(user_id: int, db: Session) -> list[str]:
    habit = db.query(Habit).filter(Habit.user_id == user_id).first()

    if not habit:
        return ["No habit set yet. Add a habit to track your progress."]

    tips = []
    ptype = (habit.productivity_type or "").lower()

    if ptype == "exercise":
        tips.append(f"Keep building your '{habit.habit_name}' habit — a consistent wake-up time makes morning exercise easier to sustain.")
    elif ptype in ("study", "learning"):
        tips.append(f"For your '{habit.habit_name}' habit, try tackling it right after a successful wake-up verification, while your mind is freshest.")
    elif ptype == "mindfulness":
        tips.append(f"Pair your '{habit.habit_name}' habit with your morning wake-up routine for consistency.")
    else:
        tips.append(f"Stay consistent with your '{habit.habit_name}' habit — small daily progress adds up.")

    verifications = (
        db.query(WakeupVerification)
        .filter(WakeupVerification.user_id == user_id)
        .order_by(WakeupVerification.started_at.desc())
        .limit(10)
        .all()
    )
    if verifications:
        success_rate = sum(1 for v in verifications if v.status == "success") / len(verifications)
        if success_rate < 0.5:
            tips.append("Your wake-up consistency is low, which may be affecting your habit progress. Focus on stabilizing your wake time first.")

    return tips


@router.get("/{user_id}")
def get_recommendation(
    user_id: int,
    db: Session = Depends(get_db)
):

    latest = (
        db.query(Analytics)
        .filter(Analytics.user_id == user_id)
        .order_by(Analytics.id.desc())
        .first()
    )

    if latest is None:
        return {
            "message": "No analytics found"
        }

    recommendations = []

    if latest.snooze_count >= 3:
        recommendations.append("Reduce snoozing.")

    if latest.completion_time > 30:
        recommendations.append("Try easier challenges.")

    if latest.success:
        recommendations.append("Excellent consistency! Keep it up.")

    if not recommendations:
        recommendations.append("Maintain your current routine.")

    return {
        "user_id": user_id,
        "recommendations": recommendations
    }


@router.get("/{user_id}/full")
def get_full_recommendation(
    user_id: int,
    db: Session = Depends(get_db)
):
    return {
        "user_id": user_id,
        "sleep": get_sleep_recommendations(user_id, db),
        "wake_up": get_wakeup_recommendations(user_id, db),
        "productivity": get_productivity_recommendations(user_id, db),
        "habit": get_habit_recommendations(user_id, db),
    }
