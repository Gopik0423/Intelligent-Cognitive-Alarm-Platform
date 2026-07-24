def calculate_habit_score(
    wakeup_consistency,
    challenge_completion,
    snooze_reduction,
    sleep_schedule_adherence,
):

    score = (
        wakeup_consistency * 0.35
        + challenge_completion * 0.25
        + snooze_reduction * 0.20
        + sleep_schedule_adherence * 0.20
    )

    return round(score, 2)
