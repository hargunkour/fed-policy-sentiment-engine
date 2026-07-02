"""
The FastAPI application. Defines the HTTP routes the frontend will call.
Run locally with: uvicorn backend.main:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.db import get_connection

app = FastAPI(title="FOMC Sentiment Dashboard API")

# CORS lets frontend (running on a different URL/port) call this API.
# Without this, browsers block the request for security reasons.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #  wide open is fine
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/meetings")
def get_meetings():
    """Returns every FOMC meeting date in the database, most recent first."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT date, filename, word_count FROM meetings ORDER BY date DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/meetings/{date}/sentiment")
def get_meeting_sentiment(date: str):
    """
    Returns the top 10 most positive and top 10 most negative n-grams
    for one meeting, ranked by final_adjusted_sentiment.
    """
    conn = get_connection()
    meeting = conn.execute("SELECT id FROM meetings WHERE date = ?", (date,)).fetchone()
    if not meeting:
        conn.close()
        raise HTTPException(status_code=404, detail=f"No meeting found for date {date}")

    top_positive = conn.execute(
        """
        SELECT ngram, final_adjusted_sentiment FROM ngram_sentiments
        WHERE meeting_id = ? ORDER BY final_adjusted_sentiment DESC LIMIT 10
        """,
        (meeting["id"],),
    ).fetchall()

    top_negative = conn.execute(
        """
        SELECT ngram, final_adjusted_sentiment FROM ngram_sentiments
        WHERE meeting_id = ? ORDER BY final_adjusted_sentiment ASC LIMIT 10
        """,
        (meeting["id"],),
    ).fetchall()

    conn.close()
    return {
        "date": date,
        "top_positive": [dict(r) for r in top_positive],
        "top_negative": [dict(r) for r in top_negative],
    }


@app.get("/sentiment/trend")
def get_sentiment_trend(ngram: str):
    """
    Returns the full time series of normalized_sentiment for one n-gram
    across all meetings, e.g. GET /sentiment/trend?ngram=inflation
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT m.date, s.normalized_sentiment
        FROM ngram_sentiments s
        JOIN meetings m ON m.id = s.meeting_id
        WHERE s.ngram = ?
        ORDER BY m.date ASC
        """,
        (ngram.lower(),),
    ).fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail=f"No data found for ngram '{ngram}'")

    return [dict(row) for row in rows]


@app.get("/sentiment/overview")
def get_sentiment_overview():
    """
    Returns one aggregate sentiment score per meeting (average of
    final_adjusted_sentiment across all n-grams in that meeting) — this
    powers the big-picture hawkish/dovish trend line.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT m.date, AVG(s.final_adjusted_sentiment) AS overall_sentiment
        FROM ngram_sentiments s
        JOIN meetings m ON m.id = s.meeting_id
        GROUP BY m.date
        ORDER BY m.date ASC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.post("/ingest")
def trigger_ingest():
    """
    Admin-only route to re-run the full pipeline. Not called by the
    deployed frontend — this is for you to manually re-populate the
    database if you add more PDFs later.
    """
    from backend.ingest import run_ingest
    run_ingest()
    return {"status": "ingest complete"}


@app.get("/")
def root():
    """Simple health check — useful for confirming the server is alive."""
    return {"status": "ok", "service": "FOMC Sentiment Dashboard API"}
