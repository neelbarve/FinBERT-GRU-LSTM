import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nlp_pipeline.sentiment.gru_model import GRUSentiment
from nlp_pipeline.sentiment.gru_tokenizer import GRUTokenizer


# -----------------------------
# Dataset wrapper (same as training)
# -----------------------------
class GRUDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        x = self.tokenizer.encode(self.texts[idx], max_len=self.max_len)
        y = self.labels[idx]
        return torch.tensor(x), torch.tensor(y)


# -----------------------------
# Evaluation function
# -----------------------------
def evaluate_gru(model_path, texts, labels, vocab_size, batch_size=32):
    tokenizer = GRUTokenizer()
    tokenizer.build_vocab(texts)

    dataset = GRUDataset(texts, labels, tokenizer)
    loader = DataLoader(dataset, batch_size=batch_size)

    model = GRUSentiment(vocab_size=vocab_size)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():
        for x, y in loader:
            logits = model(x)
            preds = torch.argmax(logits, dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)

    acc = correct / total
    print(f"GRU accuracy: {acc:.4f}")
    return acc


# -----------------------------
# Inference wrapper
# -----------------------------
def predict_gru(model_path, tokenizer, text, vocab_size):
    model = GRUSentiment(vocab_size=vocab_size)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    x = tokenizer.encode(text)
    x = torch.tensor(x).unsqueeze(0)

    with torch.no_grad():
        logits = model(x)
        pred = torch.argmax(logits, dim=1).item()

    label_map = {0: "negative", 1: "neutral", 2: "positive"}
    return {"label": label_map[pred], "score": float(torch.softmax(logits, dim=1)[0][pred])}
