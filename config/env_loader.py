import os
from dotenv import load_dotenv

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), "..", "deployment", "env", "prod.env")
    load_dotenv(env_path)

def get(key, default=None):
    return os.getenv(key, default)
