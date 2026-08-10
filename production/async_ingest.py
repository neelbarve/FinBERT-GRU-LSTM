import asyncio
from data_ingest.fetchers import fetch_news
from production.logger import get_logger

logger = get_logger("async_ingest")

async def async_fetch():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_news)

async def ingest_batch(batch_size=20):
    articles = await async_fetch()
    logger.info(f"Fetched {len(articles)} articles asynchronously")
    return articles[:batch_size]
