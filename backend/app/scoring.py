import datetime
from sqlalchemy.orm import Session
from . import models

def calculate_daily_habit_score(
    db: Session,
    user_id: int,
    date_str: str,
    alarm_time_str: str,            # e.g., "07:00"
    actual_dismiss_time_str: str,   # e.g., "07:08" (UTC or normalized local time)
    solve_time_seconds: float,      # how long the challenge took to solve
    snooze_count: int,              # how many times user snoozed
    actual_sleep_hours: float,      # how long the user slept
    target_sleep_hours: float       # target sleep duration from profile
) -> models.HabitScoreLog:
    """
    Computes habit score based on the formula:
    Habit Score = 0.35 * Wake-Up Consistency + 0.25 * Challenge Success + 0.20 * Snooze Reduction + 0.20 * Sleep Adherence
    """
    
    # 1. Wake-Up Consistency (35%)
    # Deviation in minutes relative to preferred wake up time. Let's parse HH:MM
    try:
        alarm_h, alarm_m = map(int, alarm_time_str.split(":"))
        dismiss_h, dismiss_m = map(int, actual_dismiss_time_str.split(":"))
        
        alarm_minutes = alarm_h * 60 + alarm_m
        dismiss_minutes = dismiss_h * 60 + dismiss_m
        
        # Calculate positive deviation (oversleeping)
        deviation = max(0, dismiss_minutes - alarm_minutes)
        # Deduct 5 points per minute oversleeping
        consistency_score = max(0.0, 100.0 - (deviation * 5.0))
    except Exception:
        consistency_score = 50.0 # Default if parse error
        
    # 2. Challenge Success (25%)
    # Based on solve time. If solved under 30 seconds = 100%. Deduct 1% per second after.
    challenge_score = max(0.0, 100.0 - max(0.0, (solve_time_seconds - 30.0) * 1.5))
    
    # 3. Snooze Reduction (20%)
    # 0 snoozes = 100%, 1 = 75%, 2 = 50%, 3 = 25%, 4+ = 0%
    snooze_score = max(0.0, 100.0 - (snooze_count * 25.0))
    
    # 4. Sleep Adherence (20%)
    # Target vs actual sleep. Deduct 20 points per hour deviation.
    sleep_dev = abs(actual_sleep_hours - target_sleep_hours)
    sleep_adherence_score = max(0.0, 100.0 - (sleep_dev * 20.0))
    
    # Calculated Weighted Score
    total_habit_score = (
        0.35 * consistency_score + 
        0.25 * challenge_score + 
        0.20 * snooze_score + 
        0.20 * sleep_adherence_score
    )
    
    # Check if a score already exists for this date, if so update it, otherwise create new
    existing = db.query(models.HabitScoreLog).filter(
        models.HabitScoreLog.user_id == user_id,
        models.HabitScoreLog.date == date_str
    ).first()
    
    if existing:
        existing.consistency_score = consistency_score
        existing.completion_score = challenge_score
        existing.snooze_score = snooze_score
        existing.sleep_adherence_score = sleep_adherence_score
        existing.total_habit_score = round(total_habit_score, 2)
        score_log = existing
    else:
        score_log = models.HabitScoreLog(
            user_id=user_id,
            date=date_str,
            consistency_score=consistency_score,
            completion_score=challenge_score,
            snooze_score=snooze_score,
            sleep_adherence_score=sleep_adherence_score,
            total_habit_score=round(total_habit_score, 2)
        )
        db.add(score_log)
        
    db.commit()
    db.refresh(score_log)
    return score_log

def get_habit_score_details(db: Session, user_id: int) -> dict:
    """
    Computes aggregated habit scoring metrics, determines the overall grade,
    and formats weekly and monthly progress graphs.
    """
    scores = db.query(models.HabitScoreLog).filter(
        models.HabitScoreLog.user_id == user_id
    ).order_by(models.HabitScoreLog.date.asc()).all()

    if not scores:
        return {
            "overall_score": 100.0,
            "consistency_score": 100.0,
            "completion_score": 100.0,
            "snooze_score": 100.0,
            "sleep_adherence_score": 100.0,
            "grade": "Excellent",
            "weekly_graph": [100.0] * 7,
            "monthly_graph": [100.0] * 30
        }

    total_count = len(scores)
    avg_total = sum(s.total_habit_score for s in scores) / total_count
    avg_consistency = sum(s.consistency_score for s in scores) / total_count
    avg_completion = sum(s.completion_score for s in scores) / total_count
    avg_snooze = sum(s.snooze_score for s in scores) / total_count
    avg_sleep = sum(s.sleep_adherence_score for s in scores) / total_count

    # Determine Grade
    if avg_total >= 90:
        grade = "Excellent"
    elif avg_total >= 75:
        grade = "Good"
    elif avg_total >= 50:
        grade = "Average"
    elif avg_total >= 30:
        grade = "Poor"
    else:
        grade = "Critical"

    # Fill trends
    weekly_vals = [s.total_habit_score for s in scores[-7:]]
    monthly_vals = [s.total_habit_score for s in scores[-30:]]

    while len(weekly_vals) < 7:
        weekly_vals.insert(0, 100.0)
    while len(monthly_vals) < 30:
        monthly_vals.insert(0, 100.0)

    return {
        "overall_score": round(avg_total, 1),
        "consistency_score": round(avg_consistency, 1),
        "completion_score": round(avg_completion, 1),
        "snooze_score": round(avg_snooze, 1),
        "sleep_adherence_score": round(avg_sleep, 1),
        "grade": grade,
        "weekly_graph": [round(v, 1) for v in weekly_vals],
        "monthly_graph": [round(v, 1) for v in monthly_vals]
    }

