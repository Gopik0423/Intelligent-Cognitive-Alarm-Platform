import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from app.database import Base
from app.models import User, UserProfile, Alarm, ChallengeLog, HabitScoreLog
from app.auth import get_password_hash, verify_password
from app.challenges import create_challenge, validate_answer
from app.scoring import calculate_daily_habit_score
from app.difficulty import adapt_user_difficulty, DifficultyQLearningAgent

# Setup separate test db
TEST_DATABASE_URL = "sqlite:///./test_cognitive_alarm.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_password_hashing():
    password = "SuperSecretPassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_challenge_generation():
    # Test Math puzzle generation across levels
    for diff in ["Beginner", "Easy", "Medium", "Hard", "Expert"]:
        chal = create_challenge("math", diff)
        assert chal["type"] == "Math"
        assert "question" in chal
        assert "answer" in chal
        assert len(chal["answer"]) > 0

    # Test Riddle check
    riddle = create_challenge("riddle", "Easy")
    assert riddle["type"] == "Riddles"
    assert "answer" in riddle
    
    # Test Riddle verification (fuzzy check)
    assert validate_answer(riddle["answer"], riddle) is True
    assert validate_answer("  " + riddle["answer"].upper() + "  ", riddle) is True

def test_habit_scoring_calc(db_session):
    # Test weighted score behavior
    # 0.35 * Consistency + 0.25 * Challenge + 0.20 * Snooze + 0.20 * Sleep Adherence
    
    # Create test user
    user = User(email="test_score@alarm.com", hashed_password="hashed_placeholder", role="user")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    log = calculate_daily_habit_score(
        db=db_session,
        user_id=user.id,
        date_str="2026-07-17",
        alarm_time_str="07:00",
        actual_dismiss_time_str="07:05", # 5 minutes deviation -> Consistency = 100 - (5*5) = 75
        solve_time_seconds=30.0,         # Solve speed <= 30 -> Challenge = 100
        snooze_count=1,                  # 1 snooze -> Snooze score = 100 - 25 = 75
        actual_sleep_hours=7.5,
        target_sleep_hours=8.0           # 0.5 hour deviation -> Sleep adherence = 100 - (0.5 * 20) = 90
    )
    
    # Formula expected score:
    # 0.35 * 75 + 0.25 * 100 + 0.20 * 75 + 0.20 * 90
    # = 26.25 + 25 + 15 + 18 = 84.25
    assert log.total_habit_score == 84.25
    assert log.consistency_score == 75.0
    assert log.completion_score == 100.0
    assert log.snooze_score == 75.0

def test_adaptive_difficulty(db_session):
    # Setup test user profile
    user = User(email="test_adaptive@alarm.com", hashed_password="hashed", role="user")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    profile = UserProfile(
        user_id=user.id,
        preferred_wake_up_time="07:00",
        sleep_duration_hours=8.0,
        difficulty="Easy"
    )
    db_session.add(profile)
    db_session.commit()

    # Fast solve times and 0 snoozes should scale difficulty higher
    new_diff = adapt_user_difficulty(db_session, user.id, solve_time_seconds=10.0, snooze_count=0)
    assert new_diff == "Medium"
    
    # Slow solve time or multiple snoozes should scale difficulty back down
    new_diff = adapt_user_difficulty(db_session, user.id, solve_time_seconds=90.0, snooze_count=3)
    assert new_diff == "Easy"

def test_analytics_calculations(db_session):
    # Setup test user
    user = User(email="test_analytics@alarm.com", hashed_password="hashed", role="user")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    from app.analytics import (
        calculate_analytics_summary,
        calculate_sleep_analytics,
        calculate_snooze_analytics,
        calculate_productivity_analytics
    )

    # Initial state tests
    summary = calculate_analytics_summary(db_session, user.id)
    assert summary["average_wake_up_delay_minutes"] == 0.0
    assert summary["average_snooze_count"] == 0.0
    assert summary["challenge_success_rate"] == 100.0

    # Add challenge logs
    log1 = ChallengeLog(user_id=user.id, challenge_type="Math", difficulty="Easy", snooze_count=1, is_success=True)
    log2 = ChallengeLog(user_id=user.id, challenge_type="Memory", difficulty="Easy", snooze_count=3, is_success=True)
    db_session.add_all([log1, log2])
    db_session.commit()

    snooze_data = calculate_snooze_analytics(db_session, user.id)
    assert snooze_data["average_snoozes"] == 2.0
    assert snooze_data["total_alarms_dismissed"] == 2

def test_recommendations_generation(db_session):
    user = User(email="test_recs@alarm.com", hashed_password="hashed", role="user")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    from app.recommendations import generate_user_recommendations
    
    # Generate default recommendations
    generate_user_recommendations(db_session, user.id)
    
    from app.models import Recommendation
    recs = db_session.query(Recommendation).filter(Recommendation.user_id == user.id).all()
    assert len(recs) >= 2 # default cards inserted

def test_difficulty_streak_evaluation(db_session):
    user = User(email="test_streak@alarm.com", hashed_password="hashed", role="user")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    profile = UserProfile(
        user_id=user.id,
        preferred_wake_up_time="07:00",
        sleep_duration_hours=8.0,
        difficulty="Easy"
    )
    db_session.add(profile)
    db_session.commit()

    from app.difficulty import evaluate_adaptive_difficulty

    # 1. Test 5 consecutive successes -> scales up
    for _ in range(5):
        log = ChallengeLog(user_id=user.id, challenge_type="Math", difficulty="Easy", is_success=True)
        db_session.add(log)
    db_session.commit()

    new_diff = evaluate_adaptive_difficulty(db_session, user.id)
    assert new_diff == "Medium"

    # 2. Test 3 consecutive failures -> scales down
    for _ in range(3):
        log = ChallengeLog(user_id=user.id, challenge_type="Math", difficulty="Medium", is_success=False)
        db_session.add(log)
    db_session.commit()

    new_diff = evaluate_adaptive_difficulty(db_session, user.id)
    assert new_diff == "Easy"

