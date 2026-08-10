
# from ranking.sector_ranking import rank_sectors
# from ranking.ticker_ranking import rank_tickers
# from nlp_pipeline.sentiment.eval_gru import evaluate_gru

def normalize_label(label):
    """Map labels to numeric sentiment scores."""
    mapping = {
        "negative": -1,
        "neutral": 0,
        "positive": 1
    }
    return mapping.get(label, 0)


def combine_scores(finbert_out, gru_out=None, w_fb=0.6, w_gru=0.4):
    """
    Weighted combination of FinBERT + GRU sentiment.
    FinBERT is usually more stable → higher weight.
    """
    fb_label = finbert_out["label"]
    fb_score = finbert_out["score"]
    fb_numeric = normalize_label(fb_label)

    if gru_out is None:
        return fb_numeric, fb_label, fb_score

    gru_label = gru_out["label"]
    gru_score = gru_out["score"]
    gru_numeric = normalize_label(gru_label)

    combined_numeric = w_fb * fb_numeric + w_gru * gru_numeric
    combined_score = w_fb * fb_score + w_gru * gru_score

    # Final label from numeric score
    if combined_numeric > 0.2:
        final_label = "positive"
    elif combined_numeric < -0.2:
        final_label = "negative"
    else:
        final_label = "neutral"

    return combined_numeric, final_label, combined_score


def apply_sector_relevance(sentiment_score, sector_rel):
    """
    sector_rel ∈ [0, 1]
    If sector relevance is low → sentiment should be dampened.
    """
    return sentiment_score * sector_rel


def apply_ticker_relevance(sentiment_score, ticker_rel):
    """
    ticker_rel ∈ [0, 1]
    If ticker relevance is low → sentiment should be dampened.
    """
    return sentiment_score * ticker_rel


def apply_no_signal_logic(label, score, threshold=0.15):
    """
    If sentiment is too weak → treat as no-signal.
    """
    if abs(score) < threshold:
        return "no-signal", 0.0
    return label, score


def aggregate_sentiment(finbert_out, gru_out, sector_rel, ticker_rel):
    """
    Full unified sentiment pipeline.
    """
    numeric, label, score = combine_scores(finbert_out, gru_out)

    # Apply relevance dampening
    score = apply_sector_relevance(score, sector_rel)
    score = apply_ticker_relevance(score, ticker_rel)

    # Apply no-signal logic
    final_label, final_score = apply_no_signal_logic(label, score)

    return {
        "label": final_label,
        "score": final_score,
        "raw_label": label,
        "raw_score": score,
        "sector_rel": sector_rel,
        "ticker_rel": ticker_rel
    }
