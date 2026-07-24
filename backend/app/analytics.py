import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from typing import Dict, Any
from . import models

def calculate_analytics_summary(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Computes overall behavioral analytics summary using Pandas and NumPy.
    """
    challenge_logs = db.query(models.ChallengeLog).filter(models.ChallengeLog.user_id == user_id).all()
    habit_scores = db.query(models.HabitScoreLog).filter(models.HabitScoreLog.user_id == user_id).all()
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

    default_sleep = profile.sleep_duration_hours if profile else 8.0

    if not challenge_logs and not habit_scores:
        return {
            "average_wake_up_delay_minutes": 0.0,
            "average_snooze_count": 0.0,
            "average_sleep_duration_hours": default_sleep,
            "consistency_rate": 100.0,
            "average_solve_time_seconds": 0.0,
            "challenge_success_rate": 100.0,
            "daily_productivity_score": 100.0
        }

    # Convert to DataFrames
    c_df = pd.DataFrame([{
        "is_success": l.is_success,
        "time_taken_seconds": l.time_taken_seconds or 0.0,
        "snooze_count": l.snooze_count,
        "generated_at": l.generated_at
    } for l in challenge_logs]) if challenge_logs else pd.DataFrame()

    h_df = pd.DataFrame([{
        "consistency_score": s.consistency_score,
        "sleep_adherence_score": s.sleep_adherence_score,
        "total_habit_score": s.total_habit_score,
        "date": s.date
    } for s in habit_scores]) if habit_scores else pd.DataFrame()

    # Calculate values
    avg_snooze = float(c_df["snooze_count"].mean()) if not c_df.empty else 0.0
    avg_solve = float(c_df[c_df["is_success"]]["time_taken_seconds"].mean()) if not c_df.empty and (c_df["is_success"].sum() > 0) else 0.0
    success_rate = float((c_df["is_success"].sum() / len(c_df)) * 100.0) if not c_df.empty else 100.0

    avg_consistency = float(h_df["consistency_score"].mean()) if not h_df.empty else 100.0
    avg_sleep_val = default_sleep # approximate sleep duration mapping logic
    # Calculate delay based on consistency deviation formula.
    # Deviation = (100 - consistency_score) / 5
    avg_delay = float(((100.0 - h_df["consistency_score"]).clip(lower=0) / 5.0).mean()) if not h_df.empty else 0.0
    
    prod_score = float(h_df["total_habit_score"].mean()) if not h_df.empty else 100.0

    return {
        "average_wake_up_delay_minutes": round(avg_delay, 1),
        "average_snooze_count": round(avg_snooze, 1),
        "average_sleep_duration_hours": round(avg_sleep_val, 1),
        "consistency_rate": round(avg_consistency, 1),
        "average_solve_time_seconds": round(avg_solve, 1),
        "challenge_success_rate": round(success_rate, 1),
        "daily_productivity_score": round(prod_score, 1)
    }

def calculate_sleep_analytics(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Computes sleep duration statistics and trends.
    """
    habit_scores = db.query(models.HabitScoreLog).filter(models.HabitScoreLog.user_id == user_id).order_by(models.HabitScoreLog.date.asc()).all()
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    target_sleep = profile.sleep_duration_hours if profile else 8.0

    if not habit_scores:
        return {
            "average_sleep_duration": target_sleep,
            "sleep_adherence": 100.0,
            "duration_trend_weekly": [target_sleep] * 7,
            "duration_trend_monthly": [target_sleep] * 30
        }

    h_df = pd.DataFrame([{
        "adherence": s.sleep_adherence_score,
        "deviation": (100.0 - s.sleep_adherence_score) / 20.0, # deviation in hours
        "date": pd.to_datetime(s.date)
    } for s in habit_scores])

    # Estimated actual sleep = target_sleep - sleep_deviation (rough approximation)
    h_df["actual_sleep"] = target_sleep - h_df["deviation"]
    
    mean_adherence = float(h_df["adherence"].mean())
    mean_duration = float(h_df["actual_sleep"].mean())

    # Generate trends (using last 7 and 30 logs respectively, padded with target sleep if too short)
    weekly_vals = h_df["actual_sleep"].tail(7).tolist()
    monthly_vals = h_df["actual_sleep"].tail(30).tolist()

    while len(weekly_vals) < 7:
        weekly_vals.insert(0, target_sleep)
    while len(monthly_vals) < 30:
        monthly_vals.insert(0, target_sleep)

    return {
        "average_sleep_duration": round(mean_duration, 1),
        "sleep_adherence": round(mean_adherence, 1),
        "duration_trend_weekly": [round(v, 1) for v in weekly_vals],
        "duration_trend_monthly": [round(v, 1) for v in monthly_vals]
    }

def calculate_snooze_analytics(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Computes snooze patterns and counts.
    """
    challenge_logs = db.query(models.ChallengeLog).filter(models.ChallengeLog.user_id == user_id).order_by(models.ChallengeLog.generated_at.asc()).all()

    if not challenge_logs:
        return {
            "average_snoozes": 0.0,
            "snooze_counts": [0] * 7,
            "total_alarms_dismissed": 0
        }

    c_df = pd.DataFrame([{
        "snoozes": l.snooze_count,
        "is_success": l.is_success
    } for l in challenge_logs])

    mean_snooze = float(c_df["snoozes"].mean())
    total_dismiss = int(c_df["is_success"].sum())

    weekly_snoozes = c_df["snoozes"].tail(7).tolist()
    while len(weekly_snoozes) < 7:
        weekly_snoozes.insert(0, 0)

    return {
        "average_snoozes": round(mean_snooze, 1),
        "snooze_counts": weekly_snoozes,
        "total_alarms_dismissed": total_dismiss
    }

def calculate_productivity_analytics(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Computes challenge accuracy and cognitive speed evolution metrics.
    """
    challenge_logs = db.query(models.ChallengeLog).filter(models.ChallengeLog.user_id == user_id).order_by(models.ChallengeLog.generated_at.asc()).all()
    habit_scores = db.query(models.HabitScoreLog).filter(models.HabitScoreLog.user_id == user_id).order_by(models.HabitScoreLog.date.asc()).all()

    if not challenge_logs:
        return {
            "challenge_success_rate": 100.0,
            "average_solve_time": 0.0,
            "weekly_productivity_trend": [100.0] * 7,
            "monthly_productivity_trend": [100.0] * 30
        }

    c_df = pd.DataFrame([{
        "is_success": l.is_success,
        "time": l.time_taken_seconds or 0.0
    } for l in challenge_logs])

    success_rate = float((c_df["is_success"].sum() / len(c_df)) * 100.0)
    avg_time = float(c_df[c_df["is_success"]]["time"].mean()) if (c_df["is_success"].sum() > 0) else 0.0

    prod_trends = [float(s.total_habit_score) for s in habit_scores]
    
    weekly_trend = prod_trends[-7:]
    monthly_trend = prod_trends[-30:]

    while len(weekly_trend) < 7:
        weekly_trend.insert(0, 100.0)
    while len(monthly_trend) < 30:
        monthly_trend.insert(0, 100.0)

    return {
        "challenge_success_rate": round(success_rate, 1),
        "average_solve_time": round(avg_time, 1),
        "weekly_productivity_trend": [round(t, 1) for t in weekly_trend],
        "monthly_productivity_trend": [round(t, 1) for t in monthly_trend]
    }
