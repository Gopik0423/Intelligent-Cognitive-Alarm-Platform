def calculate_difficulty(performances):
    if not performances:
        return "Easy"

    total = len(performances)
    correct = sum(1 for p in performances if p.success)

    accuracy = (correct / total) * 100

    if accuracy >= 80:
        return "Hard"
    elif accuracy >= 50:
        return "Medium"
    else:
        return "Easy"