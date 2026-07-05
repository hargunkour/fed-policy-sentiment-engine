"""
Renders the three collapsed KPI cards (Documents Analyzed, Economic
Concepts Tracked, Average Policy Sentiment). 

"""

import streamlit as st

_CARD_TEMPLATE = """
<div class="dashboard-card" style="text-align: center; position: relative;">
    <span style="position: absolute; top: 0.75rem; right: 1rem; color: #999; font-size: 0.9rem;">⤢</span>
    <div style="color: #506FC8; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem;">{title}</div>
    <div style="font-size: 2.25rem; font-weight: 700; color: #1A1A2E;">{value}</div>
</div>
"""


def render_kpi_row(documents_analyzed: int, concepts_tracked: int, avg_sentiment: float):
    """
    documents_analyzed: count of meetings within the selected year range
    concepts_tracked: total tracked n-grams (static, from config)
    avg_sentiment: mean overall_sentiment within the selected year range
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            _CARD_TEMPLATE.format(title="Documents Analyzed", value=documents_analyzed),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            _CARD_TEMPLATE.format(title="Economic Concepts Tracked", value=f"{concepts_tracked}+"),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            _CARD_TEMPLATE.format(title="Average Policy Sentiment", value=f"{avg_sentiment:.2f}"),
            unsafe_allow_html=True,
        )