import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def evaluate_finbert(model_name="ProsusAI/finbert"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    dataset = load_dataset("financial_phrasebank", "sentences_allagree")

    correct = 0
    total = 0

    for item in dataset["test"]:
        text = item["sentence"]
        label = item["label"]  # 0=neg, 1=neutral, 2=pos

        inputs = tokenizer(text, return_tensors="pt", truncation=True)
        outputs = model(**inputs)
        logits = outputs.logits
        pred = torch.argmax(logits, dim=1).item()

        correct += int(pred == label)
        total += 1

    acc = correct / total
    print(f"FinBERT accuracy: {acc:.4f}")
    return acc

if __name__ == "__main__":
    evaluate_finbert()
