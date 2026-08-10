import csv
from config.paths import TICKER_ALIASES_PATH

def build_company_dict(csv_path=TICKER_ALIASES_PATH):
    """
    config/ticker_aliases.csv has columns {alias, ticker} — one alias per row,
    multiple rows per ticker (e.g. "apple","AAPL" / "aapl","AAPL"). This does
    NOT match the {ticker, company_name} schema config/generate_aliases writes —
    that script's output was never actually used to produce this file. Reading
    the real column names here instead of the generator's.
    """
    alias_dict = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = row["ticker"]
            alias = row["alias"]
            alias_dict.setdefault(ticker, []).append(alias)
    return alias_dict
