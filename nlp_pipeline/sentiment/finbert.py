import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class FinBERTSentiment:
    def __init__(self, model_name="ProsusAI/finbert"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def predict(self, text: str):
        if not text:
            return {"label": "neutral", "score": 0.0}

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1).detach().numpy()[0]

        labels = ["negative", "neutral", "positive"]
        idx = probs.argmax()

        return {"label": labels[idx], "score": float(probs[idx])}

_default_model = None

def finbert_predict(text: str, model_name="ProsusAI/finbert"):
    """Module-level convenience wrapper so callers don't need to
    instantiate FinBERTSentiment themselves. Loads the model once
    and reuses it across calls."""
    global _default_model
    if _default_model is None:
        _default_model = FinBERTSentiment(model_name)
    return _default_model.predict(text)