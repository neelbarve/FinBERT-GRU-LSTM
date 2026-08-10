from transformers import pipeline

class ZeroShotSectorClassifier:
    def __init__(self, sectors):
        self.sectors = sectors
        self.clf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def classify(self, text):
        result = self.clf(text, self.sectors)
        scores = dict(zip(result["labels"], result["scores"]))
        return scores
    
    # Added based on claude recommendation for reduing API calls when classifying multiple texts
    # Needs less calls per overhead
    def classify_batch(self, texts):
        results = self.clf(texts, self.sectors)
        # HF returns one dict per input when given a list
        return [dict(zip(r["labels"], r["scores"])) for r in results]