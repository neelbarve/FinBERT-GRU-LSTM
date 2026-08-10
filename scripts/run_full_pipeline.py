from pipeline.full_pipeline import run_full_pipeline
from config.paths import ensure_dirs

def main():
    ensure_dirs()
    output = run_full_pipeline()

    print("\n=== PIPELINE COMPLETE ===")
    print("Ranking:", output["ranking"])
    print("Forecast MSE:", output["forecast_mse"])
    print("Example Prediction:", output["example_prediction"])

if __name__ == "__main__":
    main()
