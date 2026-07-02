"""
Runs the full pipeline once across every PDF in PDF_FOLDER, computes
final scores, and writes everything into the SQLite database.
Run this whenever new PDFs are added. The deployed app will NOT run this
on startup, it just reads the pre-populated database.
"""
import os
import concurrent.futures
import pandas as pd

from backend.config import PDF_FOLDER, LEXICON_PATH, ALL_NGRAMS, INCLUDE_DICT, EXCLUDE_DICT
from backend.nlp.pdf_processor import process_pdf
from backend.nlp.dictionary import load_lm_master_dictionary
from backend.nlp.sentiment import find_ngram_sentiments_master, apply_inclusion_exclusion
from backend.db import get_connection, init_db


def run_ingest():
    init_db()

    pdf_files = [
        os.path.join(PDF_FOLDER, f)
        for f in os.listdir(PDF_FOLDER)
        if f.endswith(".pdf")
    ]
    print(f"Found {len(pdf_files)} PDFs to process")

    # Parallel PDF processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_pdf, pdf_files))

    text_data_by_date = {date: text for date, text in results if date is not None}
    word_counts = {date: len(text.split()) for date, text in text_data_by_date.items()}
    filenames_by_date = {}
    for pdf_path in pdf_files:
        date, _ = process_pdf(pdf_path)
        if date:
            filenames_by_date[date] = os.path.basename(pdf_path)

    lm_lexicon = load_lm_master_dictionary(LEXICON_PATH)
    print(f"Loaded lexicon: {len(lm_lexicon)} words")

    df_all = find_ngram_sentiments_master(text_data_by_date, ALL_NGRAMS, lm_lexicon)
    print(f"Raw n-gram occurrences found: {len(df_all)}")

    # Aggregate by date and ngram (sum adjusted_sentiment across occurrences)
    df_agg = (
        df_all.groupby(["date", "ngram"])
        .agg(
            base_sentiment=("base_sentiment", "sum"),
            adjusted_sentiment=("adjusted_sentiment", "sum"),
            n=("n", "first"),
            total_words=("total_words", "first"),
        )
        .reset_index()
    )

    # Apply include/exclude adjustments per date
    final_scores = []
    for date, group in df_agg.groupby("date"):
        adjusted_lookup = dict(zip(group["ngram"], group["adjusted_sentiment"]))
        for _, row in group.iterrows():
            final_adj = apply_inclusion_exclusion(row, adjusted_lookup, INCLUDE_DICT, EXCLUDE_DICT)
            normalized = final_adj / row["total_words"] if row["total_words"] else 0
            final_scores.append({
                "date": date,
                "ngram": " ".join(row["ngram"]),
                "n_size": row["n"],
                "base_sentiment": row["base_sentiment"],
                "adjusted_sentiment": row["adjusted_sentiment"],
                "final_adjusted_sentiment": final_adj,
                "normalized_sentiment": normalized,
            })

    df_final = pd.DataFrame(final_scores)
    print(f"Final scored rows: {len(df_final)}")

    # --- Write to database ---
    conn = get_connection()
    cursor = conn.cursor()

    for date in text_data_by_date:
        cursor.execute(
            """
            INSERT OR REPLACE INTO meetings (date, filename, word_count)
            VALUES (?, ?, ?)
            """,
            (date, filenames_by_date.get(date, ""), word_counts.get(date, 0)),
        )
    conn.commit()

    # Build a lookup from date -> meeting_id
    cursor.execute("SELECT id, date FROM meetings")
    meeting_ids = {row["date"]: row["id"] for row in cursor.fetchall()}

    # Clear old ngram rows for meetings we're re-ingesting, then insert fresh ones
    for date in text_data_by_date:
        cursor.execute("DELETE FROM ngram_sentiments WHERE meeting_id = ?", (meeting_ids[date],))

    for _, row in df_final.iterrows():
        cursor.execute(
            """
            INSERT INTO ngram_sentiments
                (meeting_id, ngram, n_size, base_sentiment, adjusted_sentiment,
                 final_adjusted_sentiment, normalized_sentiment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                meeting_ids[row["date"]],
                row["ngram"],
                int(row["n_size"]),
                float(row["base_sentiment"]),
                float(row["adjusted_sentiment"]),
                float(row["final_adjusted_sentiment"]),
                float(row["normalized_sentiment"]),
            ),
        )

    conn.commit()
    conn.close()
    print("Ingest complete. Database populated.")


if __name__ == "__main__":
    run_ingest()
