from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "user" # user, coach, admin

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Profile Schemas
class UserProfileSchema(BaseModel):
    preferred_wake_up_time: str
    sleep_duration_hours: float
    time_zone: str
    difficulty: str
    productivity_goals: str
    habit_preferences: str

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    preferred_wake_up_time: Optional[str] = None
    sleep_duration_hours: Optional[float] = None
    time_zone: Optional[str] = None
    difficulty: Optional[str] = None
    productivity_goals: Optional[str] = None
    habit_preferences: Optional[str] = None

# Alarm Schemas
class AlarmCreate(BaseModel):
    time: str = Field(..., description="Time of the alarm in HH:MM format")
    label: Optional[str] = "Alarm"
    is_active: Optional[bool] = True
    is_smart_adaptive: Optional[bool] = False
    days_of_week: Optional[str] = "Monday,Tuesday,Wednesday,Thursday,Friday"
    alarm_type: Optional[str] = "Weekday"

class AlarmUpdate(BaseModel):
    time: Optional[str] = None
    label: Optional[str] = None
    is_active: Optional[bool] = None
    is_smart_adaptive: Optional[bool] = None
    days_of_week: Optional[str] = None
    alarm_type: Optional[str] = None

class AlarmOut(BaseModel):
    id: int
    user_id: int
    time: str
    label: str
    is_active: bool
    is_smart_adaptive: bool
    days_of_week: str
    alarm_type: str

    class Config:
        from_attributes = True

# Challenge Log Schemas
class ChallengeCreate(BaseModel):
    challenge_type: str
    difficulty: str

class ChallengeSolve(BaseModel):
    time_taken_seconds: float
    snooze_count: int
    is_success: bool
    answers: Optional[list] = None # answers submitted (for audit if needed)

class ChallengeLogOut(BaseModel):
    id: int
    user_id: int
    challenge_type: str
    difficulty: str
    generated_at: datetime
    solved_at: Optional[datetime] = None
    time_taken_seconds: Optional[float] = None
    snooze_count: int
    is_success: bool

    class Config:
        from_attributes = True

# Habit Score Schemas
class HabitScoreOut(BaseModel):
    id: int
    user_id: int
    date: str
    consistency_score: float
    completion_score: float
    snooze_score: float
    sleep_adherence_score: float
    total_habit_score: float

    class Config:
        from_attributes = True

# Dashboard Stats Schemas
class DashboardStatsOut(BaseModel):
    habit_score: float
    consistency_rate: float
    average_solve_time: float
    snooze_frequency: float
    score_history: List[HabitScoreOut]
    recent_challenges: List[ChallengeLogOut]

# Coach Client Mapper
class ClientProgressOut(BaseModel):
    client_id: int
    email: str
    current_habit_score: float
    wake_up_consistency: float
    average_solve_time: float
    snooze_frequency: float
    client_profile: UserProfileSchema

class CoachDashboardOut(BaseModel):
    clients: List[ClientProgressOut]

# Admin management
class AdminUserUpdate(BaseModel):
    role: Optional[str] = None
    is_active: Optional[bool] = None

# Difficulty History Schemas
class DifficultyHistoryOut(BaseModel):
    id: int
    user_id: int
    previous_difficulty: str
    current_difficulty: str
    reason: str
    timestamp: datetime

    class Config:
        from_attributes = True

class DifficultyStatusOut(BaseModel):
    current_difficulty: str
    history: List[DifficultyHistoryOut]

# Recommendation Schemas
class RecommendationOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    priority: str
    category: str
    reason: str
    confidence: float
    is_saved: bool
    is_dismissed: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Analytics API Response Schemas
class AnalyticsOverallSummary(BaseModel):
    average_wake_up_delay_minutes: float
    average_snooze_count: float
    average_sleep_duration_hours: float
    consistency_rate: float
    average_solve_time_seconds: float
    challenge_success_rate: float
    daily_productivity_score: float

class AnalyticsSleepSummary(BaseModel):
    average_sleep_duration: float
    sleep_adherence: float
    duration_trend_weekly: List[float]
    duration_trend_monthly: List[float]

class AnalyticsSnoozeSummary(BaseModel):
    average_snoozes: float
    snooze_counts: List[int]
    total_alarms_dismissed: int

class AnalyticsProductivitySummary(BaseModel):
    challenge_success_rate: float
    average_solve_time: float
    weekly_productivity_trend: List[float]
    monthly_productivity_trend: List[float]

