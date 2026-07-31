from datetime import date


def calculate_age(date_of_birth: date) -> int:
    """Return a user's completed age in years."""
    today = date.today()
    return today.year - date_of_birth.year - (
        (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    )


def difficulty_for_age(date_of_birth: date) -> str:
    age = calculate_age(date_of_birth)

    if age <= 7:
        return "Easy"
    elif age <= 12:
        return "Easy"
    elif age <= 17:
        return "Medium"
    else:
        return "Easy"
