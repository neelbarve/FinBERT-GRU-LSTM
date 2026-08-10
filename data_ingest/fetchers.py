import requests

# # -----------------------------
# # NewsAPI: top-headlines (free)
# # -----------------------------
# def fetch_news_newsapi_top(api_key: str, query: str):
#     url = "https://newsapi.org/v2/top-headlines"
#     params = {
#         "q": query,
#         "language": "en",
#         "pageSize": 100,
#         "apiKey": api_key
#     }
#     r = requests.get(url, params=params, timeout=30)
#     r.raise_for_status()
#     data = r.json()
#     return data.get("articles", [])


# # -----------------------------
# # Finnhub: company-news
# # -----------------------------
# def fetch_news_finnhub(api_key: str, symbol: str, from_dt, to_dt):
#     url = "https://finnhub.io/api/v1/company-news"
#     params = {
#         "symbol": symbol,
#         "from": from_dt.strftime("%Y-%m-%d"),
#         "to": to_dt.strftime("%Y-%m-%d"),
#         "token": api_key
#     }
#     r = requests.get(url, params=params, timeout=30)
#     r.raise_for_status()
#     return r.json()

from production.logger import get_logger
logger = get_logger("fetchers")

def fetch_news_newsapi_top(api_key: str, query: str):
    """
    Uses /v2/everything rather than /v2/top-headlines: top-headlines is a
    small, curated, country/category-filtered feed, and filtering it by a
    generic keyword (e.g. "market") with no country param reliably returns
    0 results. /v2/everything is NewsAPI's keyword-search endpoint over
    their full article index and is the correct fit for this use case.
    """
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "en",
            "pageSize": 100,
            "sortBy": "publishedAt",
            "apiKey": api_key,
        }
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data.get("articles", [])
    except Exception as e:
        logger.error(f"NewsAPI fetch failed: {e}")
        return []

def fetch_news_finnhub(api_key: str, symbol: str, from_dt, to_dt):
    try:
        url = "https://finnhub.io/api/v1/company-news"
        params = {
            "symbol": symbol,
            "from": from_dt.strftime("%Y-%m-%d"),
            "to": to_dt.strftime("%Y-%m-%d"),
            "token": api_key,
        }
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"Finnhub fetch failed: {e}")
        return []


def fetch_news(query: str = "market", symbol: str = "AAPL", days_back: int = 1):
    """
    Convenience wrapper aggregating both sources with sensible defaults,
    mirroring the fetch logic in pipeline/full_pipeline.py step 1.
    Used by production/async_ingest.py (run in a thread executor since
    it's a blocking/sync call under the hood).
    Returns raw (unnormalized) articles — pass through normalize_article()
    before use, same as the synchronous pipeline does.
    """
    import os
    from datetime import datetime, timedelta, timezone

    news_key = os.getenv("NEWSAPI_KEY")
    finnhub_key = os.getenv("FINNHUB_KEY")

    to_dt = datetime.now(timezone.utc)
    from_dt = to_dt - timedelta(days=days_back)

    articles = []
    articles += fetch_news_newsapi_top(news_key, query)
    articles += fetch_news_finnhub(finnhub_key, symbol, from_dt, to_dt)
    return articles
