import spacy

class FinNER:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_trf")
        except:
            self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text):
        doc = self.nlp(text)
        ents = []
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                ents.append(ent.text)
        return ents
