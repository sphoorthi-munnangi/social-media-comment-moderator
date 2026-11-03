# Category-specific thresholds selected during model development
CATEGORY_THRESHOLDS = {
    "toxic": 0.50,
    "severe_toxic": 0.25,
    "obscene": 0.50,
    "threat": 0.20,
    "insult": 0.45,
    "identity_hate": 0.20
}

# High-confidence cutoff selected during moderation policy analysis
HIDE_CUTOFF = 0.90


def get_moderation_action(probabilities):
    """
    Convert harmful-content probabilities into a moderation action.

    Returns:
        ALLOW
        REVIEW
        HIDE_CANDIDATE
    """

    predicted_harmful = False

    for label, threshold in CATEGORY_THRESHOLDS.items():
        if probabilities[label] >= threshold:
            predicted_harmful = True
            break

    if not predicted_harmful:
        return "ALLOW"

    max_probability = max(probabilities.values())

    if max_probability >= HIDE_CUTOFF:
        return "HIDE_CANDIDATE"

    return "REVIEW"