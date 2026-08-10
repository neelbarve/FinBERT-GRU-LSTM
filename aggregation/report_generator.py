

def select_top_sectors(sector_scores, top_n=2):
    """
    sector_scores: dict {sector: score}
    """
    ranked = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]


def select_top_tickers(ticker_scores, top_n=3):
    """
    ticker_scores: dict {ticker: score}
    """
    ranked = sorted(ticker_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]


def generate_report(article, sentiment_out, sector_scores, ticker_scores):
    """
    article: dict with keys {title, url, published_at}
    sentiment_out: unified sentiment dict from aggregator
    sector_scores: dict {sector: score}
    ticker_scores: dict {ticker: score}
    """

    top_sectors = select_top_sectors(sector_scores)
    top_tickers = select_top_tickers(ticker_scores)

    return {
        "article_title": article.get("title"),
        "article_url": article.get("url"),
        "published_at": article.get("published_at"),

        "sentiment_label": sentiment_out["label"],
        "sentiment_score": sentiment_out["score"],
        "raw_label": sentiment_out["raw_label"],
        "raw_score": sentiment_out["raw_score"],
        "sector_relevance": sentiment_out["sector_rel"],
        "ticker_relevance": sentiment_out["ticker_rel"],

        "top_sectors": [
            {"sector": s, "score": sc} for s, sc in top_sectors
        ],

        "top_tickers": [
            {"ticker": t, "score": sc} for t, sc in top_tickers
        ]
    }
