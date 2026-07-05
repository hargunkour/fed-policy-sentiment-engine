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
):

    # Home button
    _, home_col = st.columns([8,1])
    with home_col:
        if st.button("🏠 Home", key=f"home_{view}"):
            go_to("home")

    st.markdown(
        f"""
        <h2 style="
            text-align:center;
            color:#506FC8;
            margin-bottom:2rem;
        ">
            {_TITLES[view]}
        </h2>
        """,
        unsafe_allow_html=True,
    )

    left, centre, right = st.columns([1,6,1])

    # LEFT ARROW
    with left:
        st.markdown('<div class="arrow-column">', unsafe_allow_html=True)

        if view in _PREV:
            if st.button("←", key=f"prev_{view}"):
                go_to(_PREV[view])

        st.markdown("</div>", unsafe_allow_html=True)

    # INFO CARD
    with centre:

        if view == "kpi1":
            _render_documents_analyzed(meetings, year_range)

        elif view == "kpi2":
            _render_concepts_tracked(all_ngrams)

        elif view == "kpi3":
            _render_avg_sentiment()

    # RIGHT ARROW
    with right:
        st.markdown('<div class="arrow-column">', unsafe_allow_html=True)

        if view in _NEXT:
            if st.button("→", key=f"next_{view}"):
                go_to(_NEXT[view])

    st.markdown("</div>", unsafe_allow_html=True)

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


def _render_concepts_tracked(all_ngrams: dict):
    unigrams = len(all_ngrams.get(1, []))
    bigrams = len(all_ngrams.get(2, []))
    trigrams = len(all_ngrams.get(3, []))

    st.markdown(
        f"""
        <div class="kpi-detail-inner-card">
            <div class="kpi-detail-row"><span>Unigrams</span><b>{unigrams}</b></div>
            <div class="kpi-detail-row"><span>Bigrams</span><b>{bigrams}</b></div>
            <div class="kpi-detail-row"><span>Trigrams</span><b>{trigrams}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "Most frequent concepts (scoped to the selected year range) require a "
        "new backend aggregation endpoint — coming in Step 5."
    )


def _render_avg_sentiment():
    # Value already computed once for the collapsed card in app.py;
    # reused here via session_state rather than recomputed.
    avg_sentiment = st.session_state.get("avg_sentiment_value", 0.0)

    st.markdown(
        f"""
        <div class="kpi-detail-inner-card">
            <div style="text-align:center; font-size:2.5rem; font-weight:700; color:#1A1A2E; margin-bottom:1rem;">
                {avg_sentiment:.2f}
            </div>
            <p style="font-size:0.95rem; color:#333;">
                The average normalized sentiment score across all analyzed FOMC
                meetings. It provides a baseline for comparing individual
                meetings and long-term shifts in monetary policy language.
            </p>
            <ul style="font-size:0.95rem; color:#333;">
                <li><b>Positive</b> → More dovish (supportive of economic growth)</li>
                <li><b>Around 0</b> → Neutral</li>
                <li><b>Negative</b> → More hawkish (focused on controlling inflation)</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )