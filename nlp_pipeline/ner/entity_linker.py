import re
from rapidfuzz import fuzz, process

class EntityLinker:
    def __init__(self, alias_dict):
        self.alias_dict = alias_dict  # {"AAPL": ["Apple", "Apple Inc"], ...}

    def exact_match(self, token):
        for ticker, aliases in self.alias_dict.items():
            if token.lower() in [a.lower() for a in aliases]:
                return ticker
        return None

    def token_overlap(self, token):
        best = process.extractOne(
            token,
            [a for aliases in self.alias_dict.values() for a in aliases],
            scorer=fuzz.token_sort_ratio
        )
        if best and best[1] > 85:
            # find which ticker this alias belongs to
            for ticker, aliases in self.alias_dict.items():
                if best[0] in aliases:
                    return ticker
        return None

    def link(self, token):
        # Priority 1: exact match
        t = self.exact_match(token)
        if t:
            return t

        # Priority 2: token overlap
        t = self.token_overlap(token)
        if t:
            return t

        return None
