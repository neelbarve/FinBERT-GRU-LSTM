import asyncio

from production.logger import get_logger
from production.error_handler import safe_execute
from production.retry import retry
from production.model_registry import register_model
from production.async_ingest import ingest_batch

from pipeline.full_pipeline import run_full_pipeline
from config.paths import ensure_dirs, FORECAST_MODEL_PATH

logger = get_logger("production_pipeline")

async def main():
    ensure_dirs()

    logger.info("Starting async ingestion...")
    articles = await ingest_batch(batch_size=25)

    logger.info("Running full pipeline with production guards...")
    output = safe_execute(run_full_pipeline, articles)

    logger.info("Registering forecast model...")
    register_model("forecast_mlp", FORECAST_MODEL_PATH)

    logger.info("Pipeline complete.")
    logger.info(f"Ranking: {output['ranking']}")
    logger.info(f"MSE: {output['forecast_mse']}")
    logger.info(f"Example Prediction: {output['example_prediction']}")

if __name__ == "__main__":
    asyncio.run(main())
