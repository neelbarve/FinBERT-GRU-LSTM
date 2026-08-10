import torch

from forecasting.model import ForecastMLP
from config.paths import FORECAST_MODEL_PATH
from forecasting.features import build_features

def forecast_single(article, model_path=FORECAST_MODEL_PATH):
    """
    article: unified sentiment dict with metadata
    returns predicted future_return
    """
    x = build_features(article)
    x = torch.tensor(x, dtype=torch.float32).unsqueeze(0)

    model = ForecastMLP(input_dim=x.shape[1])
    model.load_state_dict(torch.load(model_path))
    model.eval()

    with torch.no_grad():
        pred = model(x).item()

    return pred
