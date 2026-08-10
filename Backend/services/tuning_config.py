"""
tuning_config.py

Model Optimization.

Honest framing: there's no real usage data yet to statistically "optimize"
these values against, so this is not data-driven tuning. What this does is
consolidate every previously-scattered magic number (thresholds, weights,
streak lengths) from across the difficulty engine, behavioral analytics,
and habit score modules into one documented, named location.

Before this, tuning any of these meant hunting through 3+ files and hoping
you found every hardcoded copy. Now there's exactly one place to change a
value, with a comment explaining what it controls and why the current
default was chosen. Once the app has real usage data, this is also the
single place a future data-driven optimization pass would update.
"""

# --- Adaptive Difficulty Engine (services/adaptive_engine.py) ---
DIFFICULTY_MIN_LEVEL = 1
DIFFICULTY_MAX_LEVEL = 4
CORRECT_STREAK_TO_LEVEL_UP = 3   # consecutive correct answers needed to level up
FAIL_STREAK_TO_LEVEL_DOWN = 2    # consecutive wrong answers needed to level down

# Secondary accuracy-based signal (informational only, see estimate_accuracy_level)
ACCURACY_HARD_THRESHOLD = 80     # overall accuracy % at/above which "Hard" is suggested
ACCURACY_MEDIUM_THRESHOLD = 50   # overall accuracy % at/above which "Medium" is suggested

# --- Behavioral Analytics (services/behavioral_analytics.py) ---
MIN_RECORDS_FOR_TREND = 4        # minimum attempts before trying to detect a trend at all
TREND_THRESHOLD = 5.0            # min change (percentage-scale metrics) to call it a real trend
SNOOZE_TREND_THRESHOLD = 1.0     # min change (raw snooze_count, 0-6ish scale) for a real trend
# NOTE: these two thresholds are on different scales on purpose -- accuracy/
# consistency are percentages (0-100), snooze_count is a small raw number.
# A single shared threshold previously caused snooze trends to never fire
# (see the fixed bug in behavioral_analytics.py); keep them separate.

# --- Habit Score weighted formula (services/habit_score.py) ---
# Per the original project design doc: Wake-Up Consistency 35%, Challenge
# Completion 25%, Snooze Reduction 20%, Sleep Schedule Adherence 20%.
HABIT_SCORE_WEIGHT_WAKEUP_CONSISTENCY = 0.35
HABIT_SCORE_WEIGHT_CHALLENGE_COMPLETION = 0.25
HABIT_SCORE_WEIGHT_SNOOZE_REDUCTION = 0.20
HABIT_SCORE_WEIGHT_SLEEP_SCHEDULE_ADHERENCE = 0.20
