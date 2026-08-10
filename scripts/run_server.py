import uvicorn
from deployment.app import app
from deployment.scheduler import start_scheduler

if __name__ == "__main__":
    start_scheduler()
    uvicorn.run(app, host="0.0.0.0", port=8000)
