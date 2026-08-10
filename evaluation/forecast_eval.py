
from nlp_pipeline.sentiment.eval_gru import evaluate_gru
from nlp_pipeline.sentiment.eval_finbert import evaluate_finbert

import torch

from forecasting.model import ForecastMLP
from config.paths import FORECAST_MODEL_PATH

def eval_forecast(X, y, model_path=FORECAST_MODEL_PATH):
    model = ForecastMLP(input_dim=len(X[0]))
    model.load_state_dict(torch.load(model_path))
    model.eval()

    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

    with torch.no_grad():
        preds = model(X)
        mse = ((preds - y) ** 2).mean().item()

    print(f"Forecast MSE: {mse:.4f}")
    return mse
