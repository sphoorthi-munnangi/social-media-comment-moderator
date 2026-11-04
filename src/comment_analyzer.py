from src.model_inference import predict_probabilities
from src.moderation_policy import get_moderation_action


def analyze_comment(text):
    """
    Analyze a comment and return its harmful-content probabilities
    and recommended moderation action.
    """

    probabilities = predict_probabilities(text)
    action = get_moderation_action(probabilities)

    return {
        "probabilities": probabilities,
        "action": action
    }
