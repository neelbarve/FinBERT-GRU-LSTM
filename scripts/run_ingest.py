import os
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from datetime import datetime, timedelta, timezone

from data_ingest.fetchers import fetch_news_newsapi_top, fetch_news_finnhub
from nlp_pipeline.ner_linker import extract_entities, link_entity_to_ticker, load_alias_map
from data_ingest.normalize import normalize_article
from data_ingest.storage import save_jsonl




def main():
    # Load keys
    news_key = os.getenv("NEWSAPI_KEY")
    finnhub_key = os.getenv("FINNHUB_KEY")

    if not news_key:
        print("ERROR: Set NEWSAPI_KEY")
        return
    if not finnhub_key:
        print("ERROR: Set FINNHUB_KEY")
        return

    # Time window
    to_dt = datetime.now(timezone.utc)
    from_dt = to_dt - timedelta(days=1)

    # Load alias map for ticker linking
    alias_map = load_alias_map("config/ticker_aliases.csv")

    # -----------------------------------------
    # Stage 1: Broad news ingestion (keyword)
    # -----------------------------------------
    print("Fetching broad market news...")
    raw_news = fetch_news_newsapi_top(news_key, "market")

    # Normalize raw articles
    normalized = []
    for a in raw_news:
        norm = normalize_article(a)
        normalized.append(norm)

    # -----------------------------------------
    # Stage 2: NLP entity extraction
    # -----------------------------------------
    print("Extracting entities...")
    discovered_tickers = set()

    for article in normalized:
        text = (article.get("title", "") + " " + article.get("body", "")).strip()
        ents = extract_entities(text)

        for ent in ents:
            ticker = link_entity_to_ticker(ent["text"], alias_map)
            if ticker:
                discovered_tickers.add(ticker)

        article["entities"] = ents

    print(f"Discovered tickers: {list(discovered_tickers)}")

    # -----------------------------------------
    # Stage 3: Finnhub enrichment
    # -----------------------------------------
    enriched_articles = []

    for ticker in discovered_tickers:
        print(f"Fetching Finnhub news for {ticker}...")
        fn_news = fetch_news_finnhub(finnhub_key, ticker, from_dt, to_dt)

        for a in fn_news:
            norm = normalize_article(a)
            norm["symbol"] = ticker
            enriched_articles.append(norm)

    # -----------------------------------------
    # Stage 4: Save everything
    # -----------------------------------------
    save_jsonl("data/raw/dynamic_ingest.jsonl", enriched_articles)
    print(f"Saved {len(enriched_articles)} enriched articles.")

if __name__ == "__main__":
    main()
