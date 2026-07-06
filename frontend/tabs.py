"""
Renders the three main dashboard tabs
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from frontend.insights import generate_insights
from frontend.related_terms import get_related_terms

_TRANSPARENT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Sans"),
)


def render_meeting_overview_tab(meeting_sentiment_data: dict):
    """meeting_sentiment_data: the dict returned by GET /meetings/{date}/sentiment."""
    top_positive = meeting_sentiment_data["top_positive"][:5]
    top_negative = meeting_sentiment_data["top_negative"][:5]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 Positive Sentiment Terms")
        df_pos = pd.DataFrame(top_positive)
        if not df_pos.empty:
            fig_pos = go.Figure(go.Bar(
                x=df_pos["final_adjusted_sentiment"],
                y=df_pos["ngram"],
                orientation="h",
                marker_color="#2E7D32",
            ))
            fig_pos.update_layout(yaxis=dict(autorange="reversed"), height=320, **_TRANSPARENT_LAYOUT)
            st.plotly_chart(fig_pos, use_container_width=True)
        else:
            st.info("No positive n-grams found for this meeting.")

    with col2:
        st.subheader("Top 5 Negative Sentiment Terms")
        df_neg = pd.DataFrame(top_negative)
        if not df_neg.empty:
            fig_neg = go.Figure(go.Bar(
                x=df_neg["final_adjusted_sentiment"],
                y=df_neg["ngram"],
                orientation="h",
                marker_color="#C62828",
            ))
            fig_neg.update_layout(yaxis=dict(autorange="reversed"), height=320, **_TRANSPARENT_LAYOUT)
            st.plotly_chart(fig_neg, use_container_width=True)
        else:
            st.info("No negative n-grams found for this meeting.")

    st.markdown("#### Sentiment Insights")
    for line in generate_insights(top_positive, top_negative):
        st.markdown(f"- {line}")


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
        line=dict(color="#506FC8", width=2),
        marker=dict(size=5),
    ))

    # Recession shading — unchanged from the original implementation.
    fig_trend.add_vrect(x0="2008-01-01", x1="2009-06-30",
                         fillcolor="gray", opacity=0.15, line_width=0,
                         annotation_text="2008 Financial Crisis", annotation_position="top left")
    fig_trend.add_vrect(x0="2020-02-01", x1="2020-04-30",
                         fillcolor="gray", opacity=0.15, line_width=0,
                         annotation_text="2020 COVID Shock", annotation_position="top left")

    fig_trend.update_layout(
        xaxis_title="Meeting Date",
        yaxis_title="Overall Sentiment (Hawkish ← 0 → Dovish)",
        height=450,
        **_TRANSPARENT_LAYOUT,
    )
    st.plotly_chart(fig_trend, use_container_width=True)


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
        line=dict(color="#506FC8", width=2),
    ))
    fig_search.update_layout(
        xaxis_title="Meeting Date",
        yaxis_title=f"Normalized Sentiment: '{active_term}'",
        height=400,
        **_TRANSPARENT_LAYOUT,
    )
    st.plotly_chart(fig_search, use_container_width=True)

    st.markdown("**Related Terms**")
    related = get_related_terms(active_term, ngram_options, include_dict)
    if not related:
        st.caption("No related terms found.")
        return

    rel_cols = st.columns(len(related))
    for col, term in zip(rel_cols, related):
        with col:
            if st.button(term, key=f"related_{term}", use_container_width=True):
                st.session_state["term_explorer_active"] = term
                st.rerun()