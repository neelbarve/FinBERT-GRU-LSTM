import spacy
import pandas as pd
from rapidfuzz import fuzz

nlp = spacy.load("en_core_web_sm")

# -----------------------------------
# Load alias map (company → ticker)
# -----------------------------------
def load_alias_map(path: str):
    df = pd.read_csv(path)
    alias_map = {}
    for _, row in df.iterrows():
        alias_map[row["alias"].lower()] = row["ticker"]
    return alias_map


# -----------------------------------
# Extract named entities
# -----------------------------------
def extract_entities(text: str):
    text = text or ""
    doc = nlp(text)
    ents = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "PERSON", "GPE"]:
            ents.append({"text": ent.text, "label": ent.label_})
    return ents


# -----------------------------------
# Link entity → ticker
# -----------------------------------
def link_entity_to_ticker(entity_text: str, alias_map: dict):
    entity_text = entity_text.lower()

    # Exact match
    if entity_text in alias_map:
        return alias_map[entity_text]

    # Fuzzy match
    best_score = 0
    best_ticker = None

    for alias, ticker in alias_map.items():
        score = fuzz.partial_ratio(entity_text, alias)
        if score > 85 and score > best_score:
            best_score = score
            best_ticker = ticker

    return best_ticker
