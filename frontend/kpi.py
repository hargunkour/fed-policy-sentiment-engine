"""
Renders the three collapsed KPI cards (Documents Analyzed, Economic
Concepts Tracked, Average Policy Sentiment).

"""

import streamlit as st

from frontend.state import go_to

_CAPTIONS = {
    "kpi1": "Meeting documents in selected range",
    "kpi2": "Concepts tracked across the dictionary",
    "kpi3": "Normalized hawkish-dovish score",
}


def _render_card(title: str, value, view_name: str):
    with st.container(border=True):
        title_col, icon_col = st.columns([5, 1])
        with title_col:
            st.markdown(
                f'<div style="color:#506FC8; font-weight:600; font-size:0.95rem; '
                f'padding-top: 0.35rem;">{title}</div>',
                unsafe_allow_html=True,
            )
        with icon_col:
            if st.button("⤢", key=f"expand_{view_name}", help=f"View {title} details", use_container_width=True):
                go_to(view_name)

        st.markdown(
            f'<div style="text-align:center; font-size:2.25rem; font-weight:700; '
            f'color:#1A1A2E; margin: 0.5rem 0;">{value}</div>',
            unsafe_allow_html=True,
        )
        st.caption(_CAPTIONS[view_name])


def render_kpi_row(documents_analyzed: int, concepts_tracked: int, avg_sentiment: float):
    """
    documents_analyzed: count of meetings within the selected year range
    concepts_tracked: total tracked n-grams (static, from config)
    avg_sentiment: mean overall_sentiment within the selected year range
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        _render_card("Documents Analyzed", documents_analyzed, "kpi1")
    with col2:
        _render_card("Economic Concepts Tracked", f"{concepts_tracked}+", "kpi2")
    with col3:
        _render_card("Average Policy Sentiment", f"{avg_sentiment:.2f}", "kpi3")