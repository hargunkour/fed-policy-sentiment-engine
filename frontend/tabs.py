"""
Renders the three main dashboard tabs
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
 
from frontend.insights import generate_insights
from frontend.related_terms import get_related_terms
from frontend.theme import COLOR_POSITIVE, COLOR_NEGATIVE, COLOR_TEXT, COLOR_NEUTRAL_CONTAINER
 
_TRANSPARENT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Public Sans", color=COLOR_TEXT),
)
 
 
def _render_bar_rows(items: list[dict], color: str):
    """items: list of {'ngram': str, 'final_adjusted_sentiment': float}, already sorted."""
    if not items:
        st.info("No data found for this meeting.")
        return
 
    max_abs = max(abs(i["final_adjusted_sentiment"]) for i in items) or 1.0
    rows_html = ""
    for item in items:
        value = item["final_adjusted_sentiment"]
        pct = min(100, round(abs(value) / max_abs * 100))
        rows_html += f"""
        <div style="margin-bottom: 0.9rem;">
            <div style="display:flex; justify-content:space-between; align-items:baseline;
                        font-size:0.85rem; font-weight:600; text-transform:uppercase; letter-spacing:0.02em;">
                <span>{item['ngram']}</span>
                <span style="color:{color}; font-weight:700;">{value:+.2f}</span>
            </div>
            <div style="background:{COLOR_NEUTRAL_CONTAINER}; border-radius:4px; height:6px; margin-top:5px;">
                <div style="background:{color}; width:{pct}%; height:6px; border-radius:4px;"></div>
            </div>
        </div>
        """
    st.markdown(rows_html, unsafe_allow_html=True)
 
 
def render_meeting_overview_tab(meeting_sentiment_data: dict):
    """meeting_sentiment_data: the dict returned by GET /meetings/{date}/sentiment."""
    top_positive = meeting_sentiment_data["top_positive"][:5]
    top_negative = meeting_sentiment_data["top_negative"][:5]
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown(
            '<div class="section-label" style="margin-bottom:0.75rem;">↑ Top 5 Positive Sentiments (Dovish)</div>',
            unsafe_allow_html=True,
        )
        _render_bar_rows(top_positive, COLOR_POSITIVE)
 
    with col2:
        st.markdown(
            '<div class="section-label" style="margin-bottom:0.75rem;">↓ Top 5 Negative Sentiments (Hawkish)</div>',
            unsafe_allow_html=True,
        )
        _render_bar_rows(top_negative, COLOR_NEGATIVE)
 
    insight_lines = "".join(f"<li style='margin-bottom:0.4rem;'>{line}</li>" for line in generate_insights(top_positive, top_negative))
    st.markdown(
        f"""
        <div class="dashboard-card" style="margin-top: 1.5rem;">
            <div class="section-label" style="margin-bottom:0.5rem;">Sentiment Insights</div>
            <ul style="margin:0; padding-left:1.2rem; color:#1B1C17;">
                {insight_lines}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
 
def render_time_series_tab(df_overview: pd.DataFrame, year_range: tuple[int, int]):
    """df_overview: DataFrame from /sentiment/overview with a parsed datetime 'date' column."""
    filtered = df_overview[
        (df_overview["date"].dt.year >= year_range[0]) & (df_overview["date"].dt.year <= year_range[1])
    ]
 
    if filtered.empty:
        st.info("No data in the selected year range.")
        return
 
    fig_trend = go.Figure(go.Scatter(
        x=filtered["date"],
        y=filtered["overall_sentiment"],
        mode="lines+markers",
        line=dict(color=COLOR_TEXT, width=2),
        marker=dict(size=5, color=COLOR_TEXT),
    ))
 
    fig_trend.add_vrect(x0="2008-01-01", x1="2009-06-30",
                         fillcolor=COLOR_NEGATIVE, opacity=0.10, line_width=0,
                         annotation_text="2008 Financial Crisis", annotation_position="top left")
    fig_trend.add_vrect(x0="2020-02-01", x1="2020-04-30",
                         fillcolor=COLOR_NEGATIVE, opacity=0.10, line_width=0,
                         annotation_text="2020 COVID Shock", annotation_position="top left")
 
    fig_trend.update_layout(
        xaxis_title="Meeting Date",
        yaxis_title="Overall Sentiment (Hawkish ← 0 → Dovish)",
        height=450,
        **_TRANSPARENT_LAYOUT,
    )
    st.plotly_chart(fig_trend, use_container_width=True, theme=None)
 
 
def render_term_explorer_tab(ngram_options: list[str], include_dict: dict, fetch_trend_fn):
    """
    fetch_trend_fn: callable(ngram: str) -> DataFrame | None (already parsed
    dates), matching app.py's cached fetch_ngram_trend().
    """
    active_term = st.session_state.get("term_explorer_active", "")
 
    if not active_term:
        st.info("Select a term in the sidebar's Economic Term Search to explore it here.")
        return
 
    df_search = fetch_trend_fn(active_term)
    if df_search is None or df_search.empty:
        st.warning(f"No data found for '{active_term}'. Try another term.")
        return
 
    fig_search = go.Figure(go.Scatter(
        x=df_search["date"],
        y=df_search["normalized_sentiment"],
        mode="lines+markers",
        line=dict(color=COLOR_TEXT, width=2),
        marker=dict(size=5, color=COLOR_TEXT),
    ))
    fig_search.update_layout(
        xaxis_title="Meeting Date",
        yaxis_title=f"Normalized Sentiment: '{active_term}'",
        height=400,
        **_TRANSPARENT_LAYOUT,
    )
    st.plotly_chart(fig_search, use_container_width=True, theme=None)
 
    with st.container(border=True):
        st.markdown('<div class="section-label" style="margin-bottom:0.75rem;">Related Semantic Nodes</div>', unsafe_allow_html=True)
        related = get_related_terms(active_term, ngram_options, include_dict)
        if not related:
            st.caption("No related terms found.")
        else:
            rel_cols = st.columns(len(related))
            for col, term in zip(rel_cols, related):
                with col:
                    st.markdown('<span class="pill-marker"></span>', unsafe_allow_html=True)
                    if st.button(f"{term}  ↗", key=f"related_{term}", use_container_width=True):
                        st.session_state["term_explorer_active"] = term
                        st.rerun()