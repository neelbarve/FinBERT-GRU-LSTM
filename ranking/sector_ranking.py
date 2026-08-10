def rank_sectors(sector_scores):
    """
    sector_scores: dict {sector: score}
    returns sorted list of (sector, score)
    """
    return sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)
