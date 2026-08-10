from data_ingest.normalize import normalize_article
from data_ingest.fetchers import fetch_news_newsapi_top, fetch_news_finnhub
from datetime import datetime, timedelta, timezone
import os

from nlp_pipeline.sentiment.finbert import finbert_predict
# GRU sentiment disabled for now — no trained model/vocab exists yet
# (see nlp_pipeline/sentiment/train_gru.py). Re-enable once a model has
# actually been trained; aggregate_sentiment() already supports gru_out=None
# and falls back to FinBERT-only sentiment cleanly.

from nlp_pipeline.ner.finner import FinNER
from nlp_pipeline.ner.entity_linker import EntityLinker
from nlp_pipeline.ner.company_dict_builder import build_company_dict

from sector_classification.zero_shot import ZeroShotSectorClassifier
from sector_classification.relevance import filter_relevant
from sector_classification.taxonomy_loader import load_sector_taxonomy

from aggregation.sentiment_aggregator import aggregate_sentiment
from aggregation.report_generator import generate_report

from ranking.ranking_pipeline import run_ranking_pipeline

from forecasting.dataset_builder import build_forecast_dataset
from forecasting.train_forecast import train_forecast
from evaluation.forecast_eval import eval_forecast
from forecasting.inference import forecast_single

from pipeline.utils import extract_future_return


def run_full_pipeline(raw_articles=None):
    """
    raw_articles: optional pre-fetched, unnormalized article list (e.g. from
    production/async_ingest.py's ingest_batch()). If provided, this skips the
    pipeline's own synchronous fetch and normalizes what was passed in instead —
    otherwise the async-fetched articles would be silently discarded and
    run_full_pipeline() would re-fetch everything itself from scratch.
    """
    # 1. INGEST
    if raw_articles is None:
        news_key = os.getenv("NEWSAPI_KEY")
        finnhub_key = os.getenv("FINNHUB_KEY")

        to_dt = datetime.now(timezone.utc)
        from_dt = to_dt - timedelta(days=1)

        raw_articles = []
        raw_articles += fetch_news_newsapi_top(news_key, "market")
        raw_articles += fetch_news_finnhub(finnhub_key, "AAPL", from_dt, to_dt)

    articles = [normalize_article(a) for a in raw_articles]

    # 2. SENTIMENT + RELEVANCE
    sectors = list(load_sector_taxonomy().keys())
    sector_clf = ZeroShotSectorClassifier(sectors=sectors)

    ner = FinNER()
    linker = EntityLinker(alias_dict=build_company_dict())

    # batch sector classification once, outside the loop
    # NOTE: normalize_article() returns keys {source, title, body, url, ts, raw}
    # — NOT article_title/article_body. Use "body" here, not "article_body".
    bodies = [a["body"] for a in articles]
    all_sector_scores = sector_clf.classify_batch(bodies)

    enriched_articles = []
    for a, raw_sector_scores in zip(articles, all_sector_scores):
        finbert_out = finbert_predict(a["body"])
        gru_out = None  # no trained GRU model yet — see note above

        sector_relevance_map = filter_relevant(raw_sector_scores)

        candidates = ner.extract(a["body"])
        ticker_hits = {}
        for token in candidates:
            ticker = linker.link(token)
            if ticker:
                ticker_hits[ticker] = ticker_hits.get(ticker, 0) + 1

        if ticker_hits:
            max_hits = max(ticker_hits.values())
            ticker_relevance_map = {t: count / max_hits for t, count in ticker_hits.items()}
        else:
            ticker_relevance_map = {}

        top_sector_rel = max(sector_relevance_map.values(), default=0.0)
        top_ticker_rel = max(ticker_relevance_map.values(), default=0.0)

        unified = aggregate_sentiment(finbert_out, gru_out, top_sector_rel, top_ticker_rel)

        # unified currently has: label, score, raw_label, raw_score, sector_rel, ticker_rel
        # ranking_pipeline.py and forecasting/features.py both read "sentiment_score"
        # (not "score") — alias it here so both naming conventions used across the
        # codebase resolve to the same value without editing every consumer file.
        unified["sentiment_score"] = unified["score"]

        # carry the original article metadata forward — report_generator.py needs
        # title/url/published_at, and features.py needs article_title/article_body
        unified["article_title"] = a["title"]
        unified["article_body"] = a["body"]
        unified["article_url"] = a["url"]
        unified["published_at"] = a["ts"]

        unified["future_return"] = extract_future_return(a)
        unified["sector_relevance_map"] = sector_relevance_map
        unified["ticker_relevance_map"] = ticker_relevance_map

        enriched_articles.append(unified)

    # 3. AGGREGATION + REPORTS
    reports = []
    for a in enriched_articles:
        rep = generate_report(
            # generate_report()'s `article` param expects {title, url, published_at}
            # — the enriched dict doesn't carry those under those exact names, so
            # map them explicitly here rather than passing the whole dict.
            article={
                "title": a["article_title"],
                "url": a["article_url"],
                "published_at": a["published_at"],
            },
            sentiment_out=a,
            sector_scores=a["sector_relevance_map"],
            ticker_scores=a["ticker_relevance_map"]
        )
        reports.append(rep)

    # 4. RANKING
    ranking_out = run_ranking_pipeline(enriched_articles)

    # 5. FORECASTING
    X, y = build_forecast_dataset(enriched_articles)
    model = train_forecast(X, y, epochs=10, lr=1e-3)
    mse = eval_forecast(X, y)

    example_pred = None
    if len(enriched_articles) > 0:
        example_pred = forecast_single(enriched_articles[0])

    return {
        "reports": reports,
        "ranking": ranking_out,
        "forecast_mse": mse,
        "example_prediction": example_pred
    }