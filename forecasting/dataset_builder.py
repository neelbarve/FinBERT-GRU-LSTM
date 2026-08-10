from forecasting.features import build_features


def build_forecast_dataset(articles):
    """
    articles: list of unified sentiment dicts
    returns X (features), y (targets)
    y = future_return (must be present in article)
    """
    X = []
    y = []

    for a in articles:
        X.append(build_features(a))
        y.append(a.get("future_return", 0.0))

    return X, y
