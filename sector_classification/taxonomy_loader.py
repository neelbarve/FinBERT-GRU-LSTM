import yaml
from config.paths import SECTOR_KEYWORDS_PATH

def load_sector_taxonomy(path=SECTOR_KEYWORDS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data
