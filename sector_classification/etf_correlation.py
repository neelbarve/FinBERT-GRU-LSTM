import yfinance as yf
import numpy as np

SECTOR_ETFS = {
    "technology": "XLK",
    "finance": "XLF",
    "energy": "XLE",
    "healthcare": "XLV"
}

def compute_sector_correlation(sector, sentiment_series):
    """
    sentiment_series: list or numpy array of sentiment scores over time
    """
    etf = SECTOR_ETFS.get(sector)
    if not etf:
        return None

    data = yf.download(etf, period="6mo")
    returns = data["Close"].pct_change().dropna().values

    # Align lengths
    n = min(len(returns), len(sentiment_series))
    returns = returns[-n:]
    sentiment_series = np.array(sentiment_series[-n:])

    corr = np.corrcoef(returns, sentiment_series)[0, 1]
    return float(corr)
