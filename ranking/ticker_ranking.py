def rank_tickers(ticker_scores):
    """
    ticker_scores: dict {ticker: score}
    returns sorted list of (ticker, score)
    """
    return sorted(ticker_scores.items(), key=lambda x: x[1], reverse=True)
