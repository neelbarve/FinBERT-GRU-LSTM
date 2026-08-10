from datetime import datetime

def normalize_article(article):
    # NewsAPI format
    if "title" in article and "publishedAt" in article:
        return {
            "source": article.get("source", {}).get("name"),
            "title": article.get("title"),
            "body": article.get("content") or article.get("description"),
            "url": article.get("url"),
            "ts": article.get("publishedAt"),
            "raw": article
        }

    # Finnhub format
    if "headline" in article and "datetime" in article:
        ts = datetime.utcfromtimestamp(article["datetime"]).isoformat()
        return {
            "source": article.get("source"),
            "title": article.get("headline"),
            "body": article.get("summary"),
            "url": article.get("url"),
            "ts": ts,
            "raw": article
        }

    # Fallback
    return {
        "source": None,
        "title": None,
        "body": None,
        "url": None,
        "ts": None,
        "raw": article
    }
