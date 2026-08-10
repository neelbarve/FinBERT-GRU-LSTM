from pipeline.full_pipeline import run_full_pipeline

def run_pipeline_service(article_batch):
    # Replace ingestion with API-provided articles
    output = run_full_pipeline()
    return {
        "ranking": output["ranking"],
        "forecast_mse": output["forecast_mse"],
        "example_prediction": output["example_prediction"]
    }
