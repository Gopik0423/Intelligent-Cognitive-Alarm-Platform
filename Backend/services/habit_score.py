from services.tuning_config import (
    HABIT_SCORE_WEIGHT_WAKEUP_CONSISTENCY,
    HABIT_SCORE_WEIGHT_CHALLENGE_COMPLETION,
    HABIT_SCORE_WEIGHT_SNOOZE_REDUCTION,
    HABIT_SCORE_WEIGHT_SLEEP_SCHEDULE_ADHERENCE,
)


def calculate_habit_score(
    wakeup_consistency,
    challenge_completion,
    snooze_reduction,
    sleep_schedule_adherence,
):

    score = (
        wakeup_consistency * HABIT_SCORE_WEIGHT_WAKEUP_CONSISTENCY
        + challenge_completion * HABIT_SCORE_WEIGHT_CHALLENGE_COMPLETION
        + snooze_reduction * HABIT_SCORE_WEIGHT_SNOOZE_REDUCTION
        + sleep_schedule_adherence * HABIT_SCORE_WEIGHT_SLEEP_SCHEDULE_ADHERENCE
    )

    return round(score, 2)
