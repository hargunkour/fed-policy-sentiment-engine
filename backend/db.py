"""
Creates and connects to the SQLite database. Two tables:
One to many relationship
meetings           — one row per FOMC meeting/document processed
ngram_sentiments   — one row per n-gram found in that meeting, with scores
"""

import sqlite3
from backend.config import DATABASE_PATH

def get_connection():
    """Opens a connection to the SQLite file, creating it if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name, e.g. row["date"]
    return conn

def init_db():
    """Creates both tables if they don't already exist. Safe to run repeatedly."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE NOT NULL,
            filename TEXT NOT NULL,
            word_count INTEGER,
            processed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ngram_sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER NOT NULL,
            ngram TEXT NOT NULL,
            n_size INTEGER NOT NULL,
            base_sentiment REAL,
            adjusted_sentiment REAL,
            final_adjusted_sentiment REAL,
            normalized_sentiment REAL,
            FOREIGN KEY (meeting_id) REFERENCES meetings(id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")


if __name__ == "__main__":
    init_db()
