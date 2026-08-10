from apscheduler.schedulers.background import BackgroundScheduler
from pipeline.full_pipeline import run_full_pipeline
from production.logger import get_logger

logger = get_logger("scheduler")

def scheduled_job():
    logger.info("Running scheduled pipeline...")
    output = run_full_pipeline()
    logger.info(f"Scheduled run complete. MSE: {output['forecast_mse']}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, "interval", hours=1)
    scheduler.start()
