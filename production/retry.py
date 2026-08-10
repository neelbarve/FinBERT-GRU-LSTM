import time
from production.logger import get_logger

logger = get_logger("retry")

def retry(fn, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as e:
            logger.warning(f"Attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)
    logger.error(f"All retries failed for {fn.__name__}")
    return None
