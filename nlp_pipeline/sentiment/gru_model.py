import torch
import torch.nn as nn

class GRUSentiment(nn.Module):
    def __init__(self, vocab_size, embed_dim=128, hidden_dim=256, num_classes=3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        x = self.embedding(x)
        _, h = self.gru(x)
        logits = self.fc(h[-1])
        return logits
