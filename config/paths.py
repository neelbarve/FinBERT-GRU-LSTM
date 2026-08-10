# BASE_DIR = "finbert-gru-lstm"
# MODEL_DIR = f"{BASE_DIR}/models"
# DATA_DIR = f"{BASE_DIR}/data/raw"

import os

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Core subdirectories
CONFIG_DIR = os.path.join(BASE_DIR, "config")
AGGREGATION_DIR = os.path.join(BASE_DIR, "aggregation")
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_INGEST_DIR = os.path.join(BASE_DIR, "data_ingest")
EVALUATION_DIR = os.path.join(BASE_DIR, "evaluation")
FORECASTING_DIR = os.path.join(BASE_DIR, "forecasting")
NLP_PIPELINE_DIR = os.path.join(BASE_DIR, "nlp_pipeline")
RANKING_DIR = os.path.join(BASE_DIR, "ranking")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Common file paths
TICKER_ALIASES_PATH = os.path.join(CONFIG_DIR, "ticker_aliases.csv")
SECTOR_KEYWORDS_PATH = os.path.join(CONFIG_DIR, "sector_keywords.yaml")
NEWSAPI_INGEST = os.path.join(DATA_RAW_DIR, "newsapi_ingest.jsonl")
GRU_MODEL_PATH = os.path.join(MODELS_DIR, "gru_sentiment.pt")
FORECAST_MODEL_PATH = os.path.join(MODELS_DIR, "forecast_mlp.pt")

# Utility function
def ensure_dirs():
    """Create required directories if missing."""
    for d in [MODELS_DIR, DATA_DIR, DATA_RAW_DIR]:
        os.makedirs(d, exist_ok=True)
