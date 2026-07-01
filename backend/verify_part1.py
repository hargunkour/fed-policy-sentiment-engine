"""
Running to check the pipeline works end-to-end on 2-3 local
PDFs, with no Google Drive involved. Prints results to the terminal — no database yet.
"""

import os
from backend.config import PDF_FOLDER, LEXICON_PATH, ALL_NGRAMS, INCLUDE_DICT, EXCLUDE_DICT
from backend.nlp.pdf_processor import process_pdf
from backend.nlp.dictionary import load_lm_master_dictionary
from backend.nlp.sentiment import find_ngram_sentiments_master, apply_inclusion_exclusion

pdf_files = [
    os.path.join(PDF_FOLDER, f)
    for f in os.listdir(PDF_FOLDER)
    if f.endswith(".pdf")
]

print(f"Found {len(pdf_files)} PDF(s) in {PDF_FOLDER}")

text_data_by_date = {}
for pdf_path in pdf_files:
    date, cleaned_text = process_pdf(pdf_path)
    text_data_by_date[date] = cleaned_text
    print(f"Processed {date}: {len(cleaned_text.split())} words")

lm_lexicon = load_lm_master_dictionary(LEXICON_PATH)
print(f"Loaded LM lexicon with {len(lm_lexicon)} words")

df_all = find_ngram_sentiments_master(text_data_by_date, ALL_NGRAMS, lm_lexicon)
print(f"Found {len(df_all)} n-gram occurrences")
print(df_all.head(10))