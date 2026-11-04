from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "distilbert_model"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model.eval()


def predict_probabilities(text):
    """
    Predict harmful-content probabilities for a single comment.
    """

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=256
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.sigmoid(outputs.logits)[0].tolist()

    return {
        model.config.id2label[i]: probability
        for i, probability in enumerate(probabilities)
    }