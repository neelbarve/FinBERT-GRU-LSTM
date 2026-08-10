import logging
import os

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_PATH, exist_ok=True)

def get_logger(name="pipeline"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(os.path.join(LOG_PATH, "pipeline.log"))
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
