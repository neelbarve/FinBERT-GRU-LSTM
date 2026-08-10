def aggregate_sentiment(finbert_out, gru_out=None):
    fb_label = finbert_out["label"]
    fb_score = finbert_out["score"]

    if gru_out is None:
        return fb_label, fb_score

    # Combine FinBERT + GRU
    combined_score = (fb_score + gru_out["score"]) / 2

    return fb_label, combined_score
