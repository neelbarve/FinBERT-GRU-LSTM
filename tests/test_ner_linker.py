#from nlp_pipeline.ner_linker import link_entities
from nlp_pipeline.ner.entity_linker import EntityLinker

def test_exact_match():
    alias_dict = {"AAPL": ["Apple", "Apple Inc"], "MSFT": ["Microsoft"]}
    linker = EntityLinker(alias_dict)
    assert linker.link("Apple") == "AAPL"

def test_token_overlap():
    alias_dict = {"AAPL": ["Apple Inc"], "MSFT": ["Microsoft Corp"]}
    linker = EntityLinker(alias_dict)
    assert linker.link("Microsoft") == "MSFT"

def test_no_match():
    alias_dict = {"AAPL": ["Apple"], "MSFT": ["Microsoft"]}
    linker = EntityLinker(alias_dict)
    assert linker.link("Banana") is None
