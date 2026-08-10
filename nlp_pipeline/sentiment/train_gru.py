import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# from sentiment.gru_tokenizer import GRUTokenizer
# from sentiment.gru_model import GRUSentiment

from nlp_pipeline.sentiment.gru_model import GRUSentiment
from nlp_pipeline.sentiment.gru_tokenizer import GRUTokenizer


# -----------------------------
# Dataset wrapper
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
# Training loop
# -----------------------------
def train_gru(texts, labels, vocab_size, epochs=5, batch_size=32, lr=1e-3):
    tokenizer = GRUTokenizer()
    tokenizer.build_vocab(texts)

    dataset = GRUDataset(texts, labels, tokenizer)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = GRUSentiment(vocab_size=vocab_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    model.train()

    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0

        for x, y in loader:
            optimizer.zero_grad()

            logits = model(x)
            loss = criterion(logits, y)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            preds = torch.argmax(logits, dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)

        acc = correct / total
        print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss:.4f} | Acc: {acc:.4f}")

    # Save checkpoint
    torch.save(model.state_dict(), "models/gru_sentiment.pt")
    print("Saved GRU model → models/gru_sentiment.pt")

    return model, tokenizer
