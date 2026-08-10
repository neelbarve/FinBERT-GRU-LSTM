import os
from production.logger import get_logger

logger = get_logger("model_registry")

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

def register_model(name, path):
    logger.info(f"Registering model {name} at {path}")
    with open(os.path.join(REGISTRY_PATH, "registry.txt"), "a") as f:
        f.write(f"{name}:{path}\n")

def list_models():
    registry_file = os.path.join(REGISTRY_PATH, "registry.txt")
    if not os.path.exists(registry_file):
        return []
    with open(registry_file, "r") as f:
        return [line.strip() for line in f.readlines()]
