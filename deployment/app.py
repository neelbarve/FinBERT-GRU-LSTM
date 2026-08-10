from fastapi import FastAPI
from deployment.router import router
from deployment.monitoring import monitoring_router

app = FastAPI(
    title="FinBERT-GRU-LSTM Pipeline API",
    version="1.0.0"
)

app.include_router(router)
app.include_router(monitoring_router)
