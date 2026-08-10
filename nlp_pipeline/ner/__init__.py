from .spacy_ner import SpacyNER
from .finner import FinNER
from .entity_linker import EntityLinker
from .company_dict_builder import build_company_dict

def extract_and_link(text):
    ner = SpacyNER()
    finner = FinNER()
    alias_dict = build_company_dict()
    linker = EntityLinker(alias_dict)

    ents = set(ner.extract(text)) | set(finner.extract(text))
    linked = {ent: linker.link(ent) for ent in ents}
    return linked
