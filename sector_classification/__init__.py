from .taxonomy_loader import load_sector_taxonomy
from .zero_shot import ZeroShotSectorClassifier
from .relevance import filter_relevant
from .etf_correlation import compute_sector_correlation

def classify_sector(text, sentiment_series=None):
    taxonomy = load_sector_taxonomy()
    sectors = list(taxonomy.keys())

    # Zero-shot scores
    clf = ZeroShotSectorClassifier(sectors)
    scores = clf.classify(text)

    # Filter relevant sectors
    relevant = filter_relevant(scores, t_rel=0.35, N_min=2)

    # Optional ETF correlation
    if sentiment_series:
        correlations = {
            s: compute_sector_correlation(s, sentiment_series)
            for s in relevant.keys()
        }
        return relevant, correlations

    return relevant, None
