import pandas as pd
import numpy as np
import datetime
from sqlalchemy.orm import Session
from . import models

RECOMMENDATION_CATALOG = {
    "sleep_earlier": {
        "title": "Sleep earlier tonight",
        "description": "Adjust your bedtime to be 20-30 minutes earlier to prevent cumulative sleep debt and improve morning alertness.",
        "priority": "High",
        "category": "Sleep",
        "reason": "Sleep duration fluctuates consistently below your target duration.",
        "confidence": 88.0
    },
    "avoid_mobile": {
        "title": "Avoid using mobile before bedtime",
        "description": "Avoid blue-light emitting screens starting 45 minutes before sleep to support natural melatonin production.",
        "priority": "Medium",
        "category": "Sleep",
        "reason": "Wake-up delay indicates high sleep inertia, common with late night screen exposure.",
        "confidence": 82.0
    },
    "reduce_snoozing": {
        "title": "Reduce snoozing",
        "description": "Snoozing fragments sleep, leading to grogginess. Force yourself to sit up on the first wake call.",
        "priority": "High",
        "category": "Routine",
        "reason": "Your average snooze count is higher than 1.5 snoozes per alarm.",
        "confidence": 95.0
    },
    "increase_difficulty": {
        "title": "Increase challenge difficulty",
        "description": "Your brain has adapted to current puzzle tasks. Step up difficulty to Beginner -> Easy or Medium -> Hard.",
        "priority": "Low",
        "category": "Cognitive",
        "reason": "You solve challenges in under 15 seconds consistently with 100% accuracy.",
        "confidence": 90.0
    },
    "try_memory": {
        "title": "Try memory challenges",
        "description": "Engaging spatial and numerical recall in the morning stimulates the prefrontal cortex.",
        "priority": "Medium",
        "category": "Cognitive",
        "reason": "Your memory solve scores could benefit from active reinforcement.",
        "confidence": 78.0
    },
    "try_math": {
        "title": "Try math challenges",
        "description": "Solving arithmetic functions is one of the fastest ways to shock the cognitive nervous system awake.",
        "priority": "Medium",
        "category": "Cognitive",
        "reason": "Math challenges take you longest to resolve, meaning they provide the highest cognitive wake up stimulation.",
        "confidence": 80.0
    },
    "wake_earlier": {
        "title": "Wake up 15 minutes earlier",
        "description": "Shift your wake window slightly earlier to build a buffer for a calm morning routine.",
        "priority": "Medium",
        "category": "Routine",
        "reason": "Wake up consistency scores are below 80%.",
        "confidence": 75.0
    },
    "morning_walk": {
        "title": "Morning walk recommended",
        "description": "Get light exposure within 1 hour of waking to calibrate your circadian clock.",
        "priority": "Low",
        "category": "Habit",
        "reason": "Light exposure stops melatonin synthesis, increasing alertness.",
        "confidence": 85.0
    },
    "stay_hydrated": {
        "title": "Stay hydrated",
        "description": "Drink a full glass of water immediately upon rising to counter mild sleep dehydration.",
        "priority": "Low",
        "category": "Habit",
        "reason": "Hydration restores metabolic pace and aids cognitive focus.",
        "confidence": 92.0
    },
    "meditation": {
        "title": "Morning meditation suggested",
        "description": "Take 5 minutes of focused breathing before checking your notifications to set a calm tone.",
        "priority": "Low",
        "category": "Habit",
        "reason": "Reduces cortical stress responses triggered by loud wake alarms.",
        "confidence": 70.0
    }
}

def generate_user_recommendations(db: Session, user_id: int):
    """
    Analyzes historical data and generates customized recommendation entries in the database.
    """
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    scores = db.query(models.HabitScoreLog).filter(models.HabitScoreLog.user_id == user_id).all()
    challenges = db.query(models.ChallengeLog).filter(models.ChallengeLog.user_id == user_id).all()

    # Pre-fetch existing recommendations to avoid duplicate insertions
    existing_recs = db.query(models.Recommendation).filter(
        models.Recommendation.user_id == user_id
    ).all()
    existing_titles = {r.title for r in existing_recs}

    selected_keys = ["stay_hydrated", "avoid_mobile"] # default recommendations

    # Run data rules if we have history
    if scores:
        score_df = pd.DataFrame([{
            "consistency": s.consistency_score,
            "snooze": s.snooze_score,
            "sleep": s.sleep_adherence_score
        } for s in scores])
        
        # Check sleep adherence
        if score_df["sleep"].mean() < 80.0:
            selected_keys.append("sleep_earlier")
            
        # Check snooze frequency
        if score_df["snooze"].mean() < 75.0:
            selected_keys.append("reduce_snoozing")

        # Check consistency
        if score_df["consistency"].mean() < 80.0:
            selected_keys.append("wake_earlier")
            
    if challenges:
        c_df = pd.DataFrame([{
            "type": c.challenge_type,
            "time": c.time_taken_seconds or 0.0,
            "is_success": c.is_success
        } for c in challenges])
        
        mean_time = c_df[c_df["is_success"]]["time"].mean() if (c_df["is_success"].sum() > 0) else 0.0
        if 0 < mean_time < 15.0:
            selected_keys.append("increase_difficulty")

        # Suggest challenge based on solved time
        type_perf = c_df.groupby("type")["time"].mean()
        if not type_perf.empty:
            slowest = type_perf.idxmax()
            if slowest == "Math":
                selected_keys.append("try_math")
            else:
                selected_keys.append("try_memory")

    # Add default general wellness ones if we are under 4 recommendations
    if len(selected_keys) < 4:
        selected_keys.extend(["morning_walk", "meditation"])

    # Make selection unique
    selected_keys = list(set(selected_keys))

    # Add recommendations to database if they don't already exist
    for key in selected_keys:
        rec_data = RECOMMENDATION_CATALOG.get(key)
        if rec_data and rec_data["title"] not in existing_titles:
            new_rec = models.Recommendation(
                user_id=user_id,
                title=rec_data["title"],
                description=rec_data["description"],
                priority=rec_data["priority"],
                category=rec_data["category"],
                reason=rec_data["reason"],
                confidence=rec_data["confidence"],
                is_saved=False,
                is_dismissed=False
            )
            db.add(new_rec)
    db.commit()

def get_insights_and_recommendations(db: Session, user_id: int) -> dict:
    """
    Deprecated style helper mapping legacy endpoint to the database-driven recommendation system.
    """
    # Auto-generate first
    generate_user_recommendations(db, user_id)
    
    recs = db.query(models.Recommendation).filter(
        models.Recommendation.user_id == user_id,
        models.Recommendation.is_dismissed == False
    ).all()
    
    return {
        "insights": [r.reason for r in recs],
        "recommendations": [f"{r.title}: {r.description}" for r in recs]
    }
