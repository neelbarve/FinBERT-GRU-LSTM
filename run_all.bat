@echo off
set PYTHONPATH=%cd%
set NEWSAPI_KEY=13b66ea15fa24e90802ad540501ffb2b
set FINNHUB_KEY=d9rp23pr01qoo7o5c7i0d9rp23pr01qoo7o5c7ig

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo ============================
echo RUNNING INGESTION PIPELINE
echo ============================
python scripts\run_ingest.py

echo ============================
echo RUNNING FINBERT EVALUATION
echo ============================
python nlp_pipeline\sentiment\eval_finbert.py

echo ============================
echo RUNNING GRU EVALUATION
echo ============================
python nlp_pipeline\sentiment\eval_gru.py

echo ============================
echo RUNNING SECTOR CLASSIFICATION
echo ============================
python nlp_pipeline\sector_classifier.py

echo ============================
echo RUNNING FORECASTING
echo ============================
python scripts\run_forecast.py

echo ============================
echo STARTING API SERVER
echo ============================
uvicorn deployment.app:app --host 0.0.0.0 --port 8000 --reload

pause
