"""
Heuristic "related terms" lookup for the Term Explorer tab. 
    [it's a deterministic proxy built from data
    already in the codebase, using two signals in priority order:

    1. Aruoba-Drechsel INCLUDE_DICT entries (config.py) — terms the
        methodology already treats as related/synonymous.
    2. Other tracked n-grams of the same length that share a word with
        the search term (e.g. "oil prices" ~ "oil imports").]

Falls back to the first few tracked terms alphabetically if neither
signal produces enough candidates, so the UI never shows an empty list.
"""


def get_related_terms(term: str, ngram_options: list[str], include_dict: dict, limit: int = 3) -> list[str]:
    term_words = tuple(term.split())
    if not term_words:
        return []

    related: list[str] = []

    # Signal 1: explicit include-dict relations (keys are single strings or tuples)
    key = term_words if len(term_words) > 1 else term_words[0]
    for included in include_dict.get(key, []):
        included_str = " ".join(included) if isinstance(included, tuple) else included
        if included_str in ngram_options and included_str != term and included_str not in related:
            related.append(included_str)

    # Signal 2: other tracked terms of the same n-gram length sharing a word
    if len(related) < limit:
        for opt in ngram_options:
            if len(related) >= limit:
                break
            if opt == term or opt in related:
                continue
            if len(opt.split()) == len(term_words) and set(opt.split()) & set(term_words):
                related.append(opt)

    # Signal 3: fallback — first few tracked terms alphabetically
    if len(related) < limit:
        for opt in ngram_options:
            if len(related) >= limit:
                break
            if opt != term and opt not in related:
                related.append(opt)

    return related[:limit]