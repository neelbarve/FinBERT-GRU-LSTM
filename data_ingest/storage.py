import json
from pathlib import Path

def save_jsonl(path, items):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf8") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
