"""Decision layer that turns performance and behavioral signals into safe alarm advice."""

from services.adaptive_engine import estimate_accuracy_level
from services.behavioral_analytics import analyze_behavior
from services.challenge_selector import map_level_to_difficulty


def _add(recommendations, action: str, reason: str, priority: str):
    """Add one actionable recommendation, avoiding duplicate actions."""
    if not any(item["action"] == action for item in recommendations):
        recommendations.append({"action": action, "reason": reason, "priority": priority})


def build_alarm_intelligence(performances, difficulty_record):
    """Return explainable, validated recommendations for an alarm configuration.

    Recommendations are only emitted when their supporting signal exists.  The
    result deliberately contains no conflicting difficulty advice: a user gets
    at most one of increase, decrease, or maintain.
    """
    behavior = analyze_behavior(performances)
    current = map_level_to_difficulty(difficulty_record.difficulty_level)
    recommendations = []

    if not performances:
        _add(recommendations, "maintain_difficulty", "Collect a few challenge attempts before changing the alarm difficulty.", "low")
    else:
        accuracy_level = estimate_accuracy_level(performances)
        recent = sorted(performances, key=lambda item: item.completed_at)[-5:]
        recent_success = sum(1 for item in recent if item.success) / len(recent)

        # Difficulty changes are recommendations, not overrides: live level
        # still changes only through the streak engine.
        if accuracy_level == "Hard" and recent_success >= 0.8 and current != "Hard":
            _add(recommendations, "increase_difficulty", "Recent accuracy is consistently strong, so a harder wake-up challenge should remain engaging.", "medium")
        elif accuracy_level == "Easy" and recent_success < 0.5 and current != "Easy":
            _add(recommendations, "decrease_difficulty", "Recent challenge success is low; an easier alarm challenge can rebuild consistency.", "high")
        else:
            _add(recommendations, "maintain_difficulty", "Current challenge performance is balanced for the active difficulty.", "low")

    if behavior.get("status") == "ok":
        if behavior["snooze_trend"] == "declining":
            _add(recommendations, "reduce_snoozing", "Snoozing is increasing over time; use the alarm at a more sustainable wake time.", "high")
        if behavior["accuracy_trend"] == "declining":
            _add(recommendations, "review_challenge_load", "Accuracy is trending down; monitor the next few wake-up attempts before raising difficulty.", "medium")
        if behavior["snooze_accuracy_correlation"] is not None and behavior["snooze_accuracy_correlation"] <= -0.4:
            _add(recommendations, "limit_snoozes", "More snoozing is strongly associated with lower challenge accuracy in your history.", "high")

    return {
        "current_difficulty": current,
        "difficulty_level": difficulty_record.difficulty_level,
        "behavior": behavior,
        "recommendations": recommendations,
        "validated": True,
    }
