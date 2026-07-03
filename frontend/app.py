"""
Streamlit frontend for the FOMC Sentiment Dashboard. Calls the FastAPI
backend over HTTP and renders three panels: meeting selector, top
n-grams bar chart, and overall sentiment trend line with recession
shading.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# Reminder for self: Change this to deployed backend URL later — for now, local.
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FOMC Sentiment Dashboard", layout="wide")
st.title("FOMC Monetary Policy Sentiment Dashboard (1996–2016)")
st.caption(
    "NLP-based replication of Aruoba & Drechsel's 'Identifying Monetary "
    "Policy Shocks: A Natural Language Approach' — scoring FOMC documents for sentiment using the Loughran-McDonald Master Dictionary."
)

# --- Sidebar: meeting selector ---
st.sidebar.header("FOMC Meetings")

@st.cache_data(ttl=60)
def fetch_meetings():
    resp = requests.get(f"{BACKEND_URL}/meetings")
    resp.raise_for_status()
    return resp.json()

meetings = fetch_meetings()
meeting_dates = [m["date"] for m in meetings]

if not meeting_dates:
    st.error("No meetings found in the database. Run the ingest script first.")
    st.stop()

selected_date = st.sidebar.selectbox("Select a meeting date", meeting_dates)

# --- Main panel: top positive/negative n-grams for selected meeting ---
st.header(f"Sentiment breakdown — {selected_date}")

@st.cache_data(ttl=60)
def fetch_meeting_sentiment(date):
    resp = requests.get(f"{BACKEND_URL}/meetings/{date}/sentiment")
    resp.raise_for_status()
    return resp.json()

data = fetch_meeting_sentiment(selected_date)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Positive (Dovish-leaning) N-grams")
    df_pos = pd.DataFrame(data["top_positive"])
    if not df_pos.empty:
        fig_pos = go.Figure(go.Bar(
            x=df_pos["final_adjusted_sentiment"],
            y=df_pos["ngram"],
            orientation="h",
            marker_color="seagreen",
        ))
        fig_pos.update_layout(yaxis=dict(autorange="reversed"), height=400)
        st.plotly_chart(fig_pos, use_container_width=True)
    else:
        st.info("No positive n-grams found for this meeting.")

with col2:
    st.subheader("Top 10 Negative (Hawkish-leaning) N-grams")
    df_neg = pd.DataFrame(data["top_negative"])
    if not df_neg.empty:
        fig_neg = go.Figure(go.Bar(
            x=df_neg["final_adjusted_sentiment"],
            y=df_neg["ngram"],
            orientation="h",
            marker_color="indianred",
        ))
        fig_neg.update_layout(yaxis=dict(autorange="reversed"), height=400)
        st.plotly_chart(fig_neg, use_container_width=True)
    else:
        st.info("No negative n-grams found for this meeting.")

# --- Bottom panel: overall sentiment trend with recession shading ---
st.header("Overall Sentiment Trend, 1996–2016")

@st.cache_data(ttl=60)
def fetch_overview():
    resp = requests.get(f"{BACKEND_URL}/sentiment/overview")
    resp.raise_for_status()
    return resp.json()

overview = fetch_overview()
df_overview = pd.DataFrame(overview)
df_overview["date"] = pd.to_datetime(df_overview["date"], format="%Y_%m_%d")

fig_trend = go.Figure(go.Scatter(
    x=df_overview["date"],
    y=df_overview["overall_sentiment"],
    mode="lines+markers",
    line=dict(color="steelblue"),
))

# Recession shading 
fig_trend.add_vrect(x0="2008-01-01", x1="2009-06-30",
                     fillcolor="gray", opacity=0.2, line_width=0,
                     annotation_text="2008 Financial Crisis", annotation_position="top left")
fig_trend.add_vrect(x0="2020-02-01", x1="2020-04-30",
                     fillcolor="gray", opacity=0.2, line_width=0,
                     annotation_text="2020 COVID Shock", annotation_position="top left")

fig_trend.update_layout(
    xaxis_title="Meeting Date",
    yaxis_title="Overall Sentiment (Hawkish ← 0 → Dovish)",
    height=450,
)
st.plotly_chart(fig_trend, use_container_width=True)

# --- Search box: any n-gram's full time series ---
st.header("Search: N-gram Sentiment Over Time")
search_ngram = st.text_input("Enter an n-gram exactly as it appears (e.g. 'oil prices', 'inflation')")

if search_ngram:
    resp = requests.get(f"{BACKEND_URL}/sentiment/trend", params={"ngram": search_ngram.lower()})
    if resp.status_code == 404:
        st.warning(f"No data found for '{search_ngram}'. Try another term.")
    else:
        df_search = pd.DataFrame(resp.json())
        df_search["date"] = pd.to_datetime(df_search["date"], format="%Y_%m_%d")
        fig_search = go.Figure(go.Scatter(
            x=df_search["date"], y=df_search["normalized_sentiment"],
            mode="lines+markers", line=dict(color="darkorange"),
        ))
        fig_search.update_layout(
            xaxis_title="Meeting Date",
            yaxis_title=f"Normalized Sentiment: '{search_ngram}'",
            height=400,
        )
        st.plotly_chart(fig_search, use_container_width=True)
