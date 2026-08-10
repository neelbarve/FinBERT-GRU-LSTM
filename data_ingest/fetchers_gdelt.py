import requests
import pandas as pd
from production.logger import get_logger

logger = get_logger("gdelt_fetcher")

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

def fetch_gdelt(query="finance", max_records=50):
    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json"
    }

    try:
        r = requests.get(GDELT_URL, params=params)
        r.raise_for_status()
        data = r.json()
        return data.get("articles", [])
    except Exception as e:
        logger.error(f"GDELT fetch failed: {e}")
        return []
