def filter_relevant(sector_scores, t_rel=0.35, N_min=1):
    """
    sector_scores: {"technology": 0.82, "finance": 0.12, ...}
    t_rel: minimum score threshold
    N_min: minimum number of sectors to keep
    """
    filtered = {s: v for s, v in sector_scores.items() if v >= t_rel}

    # If too few sectors pass threshold, keep top-N_min
    if len(filtered) < N_min:
        sorted_scores = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)
        filtered = dict(sorted_scores[:N_min])

    return filtered
