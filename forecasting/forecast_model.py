import numpy as np

def build_features(article):
    """
    article: unified sentiment + relevance + metadata
    returns feature vector for forecasting model
    """
    return np.array([
        article["sentiment_score"],
        article["sector_rel"],
        article["ticker_rel"],
        len(article.get("title", "")),
        len(article.get("body", "")),
    ], dtype=float)

