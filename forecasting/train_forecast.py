import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from forecasting.model import ForecastMLP
from config.paths import FORECAST_MODEL_PATH

def train_forecast(X, y, epochs=10, lr=1e-3):
    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = ForecastMLP(input_dim=X.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    for ep in range(epochs):
        total_loss = 0.0
        for xb, yb in loader:
            optimizer.zero_grad()
            pred = model(xb)
            loss = loss_fn(pred, yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {ep+1}/{epochs} | Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), FORECAST_MODEL_PATH)
    return model
