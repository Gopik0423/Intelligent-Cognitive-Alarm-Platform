"""
report_data.py

Analytics Reports Support.

Consolidates data from across the platform (performance averages, behavioral
trends, current difficulty level, habit score breakdown) into a single
report-ready structure. This is the data backbone for any report/export
feature (PDF, Excel, dashboards) -- it doesn't render anything itself, it
just assembles clean, consistent data for something else to consume.
"""

from datetime import datetime, timezone

from models.performance import Performance
from models.difficulty import DifficultyLevel
from models.habit_score import HabitScore
from services.analytics import generate_analytics
from services.behavioral_analytics import analyze_behavior


def build_user_report(db, user_id: int) -> dict:
    performances = (
        db.query(Performance)
        .filter(Performance.user_id == user_id)
        .all()
    )

    performance_summary = generate_analytics(performances) if performances else {
        "message": "No performance data yet."
    }

    behavioral_analytics = analyze_behavior(performances) if performances else {
        "status": "not_enough_data",
        "message": "No performance data yet.",
    }

    difficulty_record = (
        db.query(DifficultyLevel)
        .filter(DifficultyLevel.user_id == user_id)
        .first()
    )

    habit_score_record = (
        db.query(HabitScore)
        .filter(HabitScore.user_id == user_id)
        .first()
    )

    return {
        "user_id": user_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "attempts_analyzed": len(performances),
        "performance_summary": performance_summary,
        "behavioral_analytics": behavioral_analytics,
        "current_difficulty_level": (
            difficulty_record.difficulty_level if difficulty_record else None
        ),
        "habit_score": (
            {
                "score": habit_score_record.habit_score,
                "wake_up_consistency": habit_score_record.wake_up_consistency,
                "challenge_completion": habit_score_record.challenge_completion,
                "snooze_reduction": habit_score_record.snooze_reduction,
                "sleep_schedule_adherence": habit_score_record.sleep_schedule_adherence,
            }
            if habit_score_record else None
        ),
    }
