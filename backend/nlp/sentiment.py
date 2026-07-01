"""
Scans cleaned FOMC text for economically meaningful n-grams and scores
each occurrence using the Loughran-McDonald lexicon:
     score the n-gram itself, plus
    the words immediately before and after it.
"""

import pandas as pd
from nltk.tokenize import word_tokenize


def _lm_score(word, lm_lexicon):
    """Look up a single word's net sentiment: +1, -1, or 0."""
    entry = lm_lexicon.get(word.upper())
    if not entry:
        return 0
    return int(entry["Positive"] > 0) - int(entry["Negative"] > 0)   # computes sentiment score (whatever side of +ve or -ve dominates)


# context-aware phrase sentiment (use scanning windows to score the n-gram itself, plus the words immediately before and after it)
def find_ngram_sentiments_master(text_data_by_date, ngrams_with_n, lm_lexicon, window=10):
    """
    text_data_by_date: {date: cleaned_text}
    ngrams_with_n: {1: singles_list, 2: doubles_list, 3: triples_list}
    Returns a DataFrame with one row per n-gram occurrence found.
    """

    rows = []

    for date, text in text_data_by_date.items():
        tokens = text.split()
        total_words = len(tokens)

        for n, ngram_list in ngrams_with_n.items():
            for i in range(len(tokens) - n + 1):
                candidate = tuple(tokens[i:i + n])
                if candidate not in ngram_list:
                    continue

                # Base sentiment of the n-gram itself
                base_sentiment = sum(_lm_score(w, lm_lexicon) for w in candidate)

                # Context window: `window` words before and after
                before_tokens = tokens[max(0, i - window):i]
                after_tokens = tokens[i + n:i + n + window]

                before_sentiment = sum(_lm_score(w, lm_lexicon) for w in before_tokens)
                after_sentiment = sum(_lm_score(w, lm_lexicon) for w in after_tokens)

                adjusted_sentiment = base_sentiment + before_sentiment + after_sentiment

                rows.append({
                    "date": date,
                    "ngram": candidate,
                    "context": " ".join(before_tokens + list(candidate) + after_tokens),
                    "base_sentiment": base_sentiment,
                    "before_sentiment": before_sentiment,
                    "after_sentiment": after_sentiment,
                    "adjusted_sentiment": adjusted_sentiment,
                    "n": n,
                    "total_words": total_words,
                })

    return pd.DataFrame(rows)


def apply_inclusion_exclusion(row, adjusted_values, include_dict, exclude_dict):
    """
    row: a row (dict-like) from the sentiment DataFrame, must have "ngram"
         and "adjusted_sentiment".
    adjusted_values: {ngram: adjusted_sentiment} lookup across the same
         meeting date, used to find related n-grams' scores.
    Returns: final_adjusted_sentiment (float)
    """
    ngram_key = row["ngram"] if len(row["ngram"]) > 1 else row["ngram"][0]
    final_score = row["adjusted_sentiment"]

    for included in include_dict.get(ngram_key, []):
        final_score += adjusted_values.get(included, 0)

    for excluded in exclude_dict.get(ngram_key, []):
        final_score -= adjusted_values.get(excluded, 0)

    return final_score
