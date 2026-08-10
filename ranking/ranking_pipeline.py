from ranking.sector_ranking import rank_sectors
from ranking.ticker_ranking import rank_tickers

def compute_sector_scores(articles):
    """
    articles: list of dicts with unified sentiment + sector relevance
    returns dict {sector: aggregated_score}
    """
    scores = {}
    for a in articles:
        for sector, rel in a["sector_relevance_map"].items():
            scores.setdefault(sector, 0)
            scores[sector] += a["sentiment_score"] * rel
    return scores


def compute_ticker_scores(articles):
    """
    articles: list of dicts with unified sentiment + ticker relevance
    returns dict {ticker: aggregated_score}
    """
    scores = {}
    for a in articles:
        for ticker, rel in a["ticker_relevance_map"].items():
            scores.setdefault(ticker, 0)
            scores[ticker] += a["sentiment_score"] * rel
    return scores


def run_ranking_pipeline(articles):
    """
    articles: list of enriched + aggregated sentiment dicts
    returns:
        top_sectors, top_tickers, sector_scores, ticker_scores
    """
    sector_scores = compute_sector_scores(articles)
    ticker_scores = compute_ticker_scores(articles)

    ranked_sectors = rank_sectors(sector_scores)
    ranked_tickers = rank_tickers(ticker_scores)

    top_sectors = ranked_sectors[:2]
    top_tickers = ranked_tickers[:3]

    return {
        "sector_scores": sector_scores,
        "ticker_scores": ticker_scores,
        "top_sectors": top_sectors,
        "top_tickers": top_tickers
    }
