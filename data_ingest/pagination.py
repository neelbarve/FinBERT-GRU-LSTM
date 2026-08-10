import time
from production.logger import get_logger

logger = get_logger("pagination")

def safe_paginate(fetch_fn, pages=5, delay=1.2):
    all_items = []

    for p in range(pages):
        try:
            batch = fetch_fn(page=p)
            if not batch:
                break
            all_items.extend(batch)
            time.sleep(delay)
        except Exception as e:
            logger.error(f"Pagination failed on page {p}: {e}")
            break

    return all_items
