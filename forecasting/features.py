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
        len(article.get("article_title", "") or ""),
        len(article.get("article_body", "") or ""),
    ], dtype=float)
