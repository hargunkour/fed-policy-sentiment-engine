"""
Loads the Loughran-McDonald Master Dictionary: a financial-text sentiment lexicon 
and turns it into a fast lookup dictionary.
"""

import pandas as pd


def load_lm_master_dictionary(filepath):
    """
    Reads the Loughran-McDonald CSV and returns a dictionary shaped like:
    {
        "INFLATION": {"Positive": 0, "Negative": 1},
        "GROWTH": {"Positive": 1, "Negative": 0},
        ...
    }
    A word is "positive" or "negative" if the its CSV column is a non-zero number.
    """
    df = pd.read_csv(filepath)

    lm_lexicon = {}
    for _, row in df.iterrows():
        word = str(row["Word"]).upper()
        lm_lexicon[word] = {
            "Positive": int(row["Positive"]) if row["Positive"] else 0,
            "Negative": int(row["Negative"]) if row["Negative"] else 0,
        }
    return lm_lexicon
