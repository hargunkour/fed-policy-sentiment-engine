"""
Deterministic, rule-based sentiment insights for the Meeting Overview tab. 
Derived directly from the top_positive/top_negative n-gram data 
already returned by GET /meetings/{date}/sentiment, using simple comparisons.
"""
 
def _pos_span(text: str) -> str:
    return f'<span class="insight-positive">{text}</span>'
 
 
def _neg_span(text: str) -> str:
    return f'<span class="insight-negative">{text}</span>'
 
 
def _quote_span(text: str) -> str:
    return f'<span class="insight-quote">&ldquo;{text}&rdquo;</span>'
 
 
def generate_insights(top_positive: list[dict], top_negative: list[dict]) -> list[str]:
    """
    top_positive / top_negative: lists of {"ngram": str, "final_adjusted_sentiment": float},
    already sorted by the backend (most positive first / most negative first).
    Returns a short list of HTML-flavored strings (safe for unsafe_allow_html=True).
    """
    if not top_positive and not top_negative:
        return ["No n-gram sentiment data available for this meeting."]
 
    insights = []
    strongest_positive = top_positive[0] if top_positive else None
    strongest_negative = top_negative[0] if top_negative else None
 
    # Dominant theme: whichever side has the single largest-magnitude term.
    if strongest_positive and strongest_negative:
        if abs(strongest_positive["final_adjusted_sentiment"]) >= abs(strongest_negative["final_adjusted_sentiment"]):
            dominant, span_fn = strongest_positive, _pos_span
        else:
            dominant, span_fn = strongest_negative, _neg_span
        insights.append(f"The dominant economic theme this meeting was {_quote_span(dominant['ngram'])}.")
    elif strongest_positive or strongest_negative:
        dominant = strongest_positive or strongest_negative
        insights.append(f"The only notable economic theme this meeting was {_quote_span(dominant['ngram'])}.")
 
    if strongest_negative:
        insights.append(
            f"Strongest hawkish signal: {_neg_span(strongest_negative['ngram'])} "
            f"({strongest_negative['final_adjusted_sentiment']:.2f})."
        )
    if strongest_positive:
        insights.append(
            f"Strongest dovish signal: {_pos_span(strongest_positive['ngram'])} "
            f"({strongest_positive['final_adjusted_sentiment']:.2f})."
        )
 
    # Unusual observation: compare total magnitude on each side to flag a skew.
    pos_magnitude = sum(abs(r["final_adjusted_sentiment"]) for r in top_positive)
    neg_magnitude = sum(abs(r["final_adjusted_sentiment"]) for r in top_negative)
 
    if pos_magnitude == 0 and neg_magnitude == 0:
        insights.append("Sentiment signals were negligible across tracked terms this meeting.")
    else:
        ratio = pos_magnitude / neg_magnitude if neg_magnitude else float("inf")
        if ratio > 1.5:
            insights.append(f"Unusual observation: {_pos_span('dovish language')} notably outweighed hawkish language this meeting.")
        elif ratio < 0.67:
            insights.append(f"Unusual observation: {_neg_span('hawkish language')} notably outweighed dovish language this meeting.")
        else:
            insights.append("Positive and negative sentiment signals were relatively balanced this meeting.")
 
    return insights