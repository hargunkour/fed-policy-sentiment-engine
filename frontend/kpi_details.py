"""
Full-page KPI detail views (kpi1 = Documents Analyzed, kpi2 = Economic
Concepts Tracked, kpi3 = Average Policy Sentiment).

render_kpi_detail() is the single entry point app.py calls.
"""

import streamlit as st

from frontend.state import go_to
from frontend.utils import year_of

_NEXT = {"kpi1": "kpi2", "kpi2": "kpi3"}
_PREV = {"kpi2": "kpi1", "kpi3": "kpi2"}


_TITLES = {
    "kpi1": "Documents Analyzed",
    "kpi2": "Economic Concepts Tracked",
    "kpi3": "Average Policy Sentiment",
}
 
 
def render_kpi_detail(
    view: str,
    meetings: list[dict],
    year_range: tuple[int, int],
    all_ngrams: dict,
    concepts_summary: dict | None = None,
):
    # --- Top row: Home only (top-right) ---
    _, home_col = st.columns([8, 1])
    with home_col:
        if st.button("Home", key="home_nav_button", icon=":material/home:"):
            go_to("home")
 
    # --- Page title ---
    st.markdown(
        f'<h2 class="font-serif" style="text-align:center; margin-top: 0.5rem;">{_TITLES[view]}</h2>',
        unsafe_allow_html=True,
    )
 
    # --- Back / content / Next, vertically centered against the card ---
    back_col, content_col, next_col = st.columns([1, 8, 1], vertical_alignment="center")
 
    with back_col:
        if view in _PREV:
            st.markdown('<span class="arrow-marker"></span>', unsafe_allow_html=True)
            if st.button("←", key=f"prev_{view}", help="Previous"):
                go_to(_PREV[view])
 
    with content_col:
        if view == "kpi1":
            _render_documents_analyzed(meetings, year_range)
        elif view == "kpi2":
            _render_concepts_tracked(concepts_summary)
        elif view == "kpi3":
            _render_avg_sentiment()
 
    with next_col:
        if view in _NEXT:
            st.markdown('<span class="arrow-marker"></span>', unsafe_allow_html=True)
            if st.button("→", key=f"next_{view}", help="Next"):
                go_to(_NEXT[view])
 
 
def _render_documents_analyzed(meetings: list[dict], year_range: tuple[int, int]):
    docs_in_range = [
        m for m in meetings
        if year_range[0] <= year_of(m["date"]) <= year_range[1]
    ]
    doc_count = len(docs_in_range)
    years_covered = (
        f"{min(year_of(m['date']) for m in docs_in_range)}–{max(year_of(m['date']) for m in docs_in_range)}"
        if docs_in_range else "N/A"
    )
    avg_len = int(sum(m["word_count"] for m in docs_in_range) / doc_count) if doc_count else 0
    total_words = sum(m["word_count"] for m in docs_in_range)
 
    st.markdown(
        f"""
        <div class="kpi-detail-inner-card">
            <div class="kpi-detail-row"><span>Documents analyzed</span><b>{doc_count}</b></div>
            <div class="kpi-detail-row"><span>Years covered</span><b>{years_covered}</b></div>
            <div class="kpi-detail-row"><span>Average document length</span><b>{avg_len:,} words</b></div>
            <div class="kpi-detail-row"><span>Total words processed</span><b>{total_words:,}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
 
def _render_concepts_tracked(concepts_summary: dict | None):
    summary = concepts_summary or {"unigrams_found": 0, "bigrams_found": 0, "trigrams_found": 0, "top_concepts": []}
    top_concepts = summary["top_concepts"]
 
    if top_concepts:
        concepts_line = ", ".join(item["ngram"] for item in top_concepts[:5])
    else:
        concepts_line = "No concepts found for the selected year range."
 
    st.markdown(
        f"""
        <div class="kpi-detail-inner-card">
            <div class="kpi-detail-row"><span>Unigrams detected</span><b>{summary['unigrams_found']}</b></div>
            <div class="kpi-detail-row"><span>Bigrams detected</span><b>{summary['bigrams_found']}</b></div>
            <div class="kpi-detail-row"><span>Trigrams detected</span><b>{summary['trigrams_found']}</b></div>
            <div style="margin-top:1rem;">
                <div class="section-label" style="margin-bottom:0.4rem;">Most frequent concepts in this range</div>
                <div style="color:#1B1C17; font-size:0.95rem;">{concepts_line}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
 
def _render_avg_sentiment():
    # Value already computed once for the collapsed card in app.py;
    # reused here via session_state rather than recomputed.
    avg_sentiment = st.session_state.get("avg_sentiment_value", 0.0)
 
    st.markdown(
        f"""
        <div class="kpi-detail-inner-card">
            <div class="font-serif" style="text-align:center; font-size:2.5rem; font-weight:700; margin-bottom:1rem;">
                {avg_sentiment:.2f}
            </div>
            <p style="font-size:0.95rem; color:#444748;">
                The average normalized sentiment score across all analyzed FOMC
                meetings. It provides a baseline for comparing individual
                meetings and long-term shifts in monetary policy language.
            </p>
            <ul style="font-size:0.95rem; color:#444748;">
                <li><b>Positive</b> → More dovish (supportive of economic growth)</li>
                <li><b>Around 0</b> → Neutral</li>
                <li><b>Negative</b> → More hawkish (focused on controlling inflation)</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
 