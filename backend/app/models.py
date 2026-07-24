import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Time, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user") # user, coach, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    alarms = relationship("Alarm", back_populates="user", cascade="all, delete-orphan")
    challenge_logs = relationship("ChallengeLog", back_populates="user", cascade="all, delete-orphan")
    habit_score_logs = relationship("HabitScoreLog", back_populates="user", cascade="all, delete-orphan")
    difficulty_history = relationship("DifficultyHistory", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    preferred_wake_up_time = Column(String, default="07:00") # "HH:MM"
    sleep_duration_hours = Column(Float, default=8.0)
    time_zone = Column(String, default="UTC")
    difficulty = Column(String, default="Easy") # Beginner, Easy, Medium, Hard, Expert
    productivity_goals = Column(Text, default="Wake up early, stay consistent")
    habit_preferences = Column(Text, default="Math,Memory") # comma-separated challenge preferences

    user = relationship("User", back_populates="profile")

class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    time = Column(String, nullable=False) # "HH:MM"
    label = Column(String, default="Alarm")
    is_active = Column(Boolean, default=True)
    is_smart_adaptive = Column(Boolean, default=False)
    days_of_week = Column(String, default="Monday,Tuesday,Wednesday,Thursday,Friday") # Comma separated: Monday, Tuesday...
    alarm_type = Column(String, default="Weekday") # Daily, Weekday, Weekend, One-Time, Smart Adaptive

    user = relationship("User", back_populates="alarms")

class ChallengeLog(Base):
    __tablename__ = "challenge_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    challenge_type = Column(String, nullable=False) # Math, Logic, Memory, Word Games, Pattern, Riddle
    difficulty = Column(String, nullable=False) # Beginner, Easy, Medium, Hard, Expert
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    solved_at = Column(DateTime, nullable=True)
    time_taken_seconds = Column(Float, nullable=True)
    snooze_count = Column(Integer, default=0)
    is_success = Column(Boolean, default=False)

    user = relationship("User", back_populates="challenge_logs")

class HabitScoreLog(Base):
    __tablename__ = "habit_score_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(String, nullable=False) # "YYYY-MM-DD"
    consistency_score = Column(Float, default=100.0) # 0 to 100
    completion_score = Column(Float, default=100.0) # 0 to 100
    snooze_score = Column(Float, default=100.0) # 0 to 100
    sleep_adherence_score = Column(Float, default=100.0) # 0 to 100
    total_habit_score = Column(Float, default=100.0) # Weighted sum

    user = relationship("User", back_populates="habit_score_logs")

class WellnessCoachMapping(Base):
    __tablename__ = "wellness_coach_mappings"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    client_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

class DifficultyHistory(Base):
    __tablename__ = "difficulty_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    previous_difficulty = Column(String, nullable=False)
    current_difficulty = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="difficulty_history")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String, nullable=False) # High, Medium, Low
    category = Column(String, nullable=False) # Sleep, Cognitive, Habit, Routine
    reason = Column(String, nullable=False)
    confidence = Column(Float, nullable=False) # Percentage e.g. 85.0
    is_saved = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="recommendations")

