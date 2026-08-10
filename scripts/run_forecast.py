# from forecasting.train_forecast import train_forecast
# from forecasting.eval_forecast import eval_forecast
# from forecasting.dataset_builder import build_forecast_dataset
# from ranking.ranking_pipeline import run_ranking_pipeline

from config.paths import ensure_dirs
from forecasting.dataset_builder import build_forecast_dataset
from forecasting.train_forecast import train_forecast
from evaluation.forecast_eval import eval_forecast
from forecasting.inference import forecast_single

def main(articles):
    """
    articles: list of dicts with:
        - sentiment_score
        - sector_rel
        - ticker_rel
        - article_title
        - article_body
        - future_return (for training)
    """
    ensure_dirs()

    X, y = build_forecast_dataset(articles)
    model = train_forecast(X, y, epochs=10, lr=1e-3)
    mse = eval_forecast(X, y)

    print("Training complete. MSE:", mse)

    # Example inference on first article
    pred = forecast_single(articles[0])
    print("Example forecast (first article):", pred)

if __name__ == "__main__":
    # You will pass real articles from your pipeline
    dummy_articles = []
    main(dummy_articles)
