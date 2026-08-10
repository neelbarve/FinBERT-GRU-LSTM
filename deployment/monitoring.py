from fastapi import APIRouter
import time

monitoring_router = APIRouter(prefix="/monitor", tags=["monitoring"])

@monitoring_router.get("/health")
def health_check():
    return {"status": "ok", "timestamp": time.time()}

@monitoring_router.get("/ping")
def ping():
    return {"message": "pong"}
