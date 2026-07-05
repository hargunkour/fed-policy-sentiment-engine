"""
Streamlit frontend for the FOMC Sentiment Dashboard. Calls the FastAPI
backend over HTTP and renders three panels: meeting selector, top
n-grams bar chart, and overall sentiment trend line with recession
shading.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

from theme import inject_theme
from state import init_view_state, get_view, go_to

# Reminder for self: Change this to deployed backend URL later — for now, local.
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FOMC Sentiment Dashboard", layout="wide")

inject_theme()
init_view_state()

# --- Header row: title/subtitle on the left, context-aware nav button top-right ---
# On the home view this button is "FAQs" (goes to the FAQ page).
# On the FAQ view it flips to "Home" (returns to the dashboard) — never both.
current_view = get_view()

header_left, header_right = st.columns([6, 1])
with header_left:
    st.markdown(
        '<h1 class="dashboard-title">FOMC Sentiment Intelligent Dashboard</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="dashboard-subtitle">1996–2026 Monetary Policy Analysis</p>',
        unsafe_allow_html=True,
    )
with header_right:
    st.write("")  # vertical spacer to align button with title
    if current_view == "faq":
        if st.button("🏠 Home", key="home_nav_button"):
            go_to("home")
    else:
        if st.button("❓ FAQs", key="faq_nav_button"):
            go_to("faq")

# --- FAQ placeholder view (full content comes in Step 9) ---
if current_view == "faq":
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("FAQs")
    st.write("FAQ content will be built in a later step.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- Everything below this only renders on the "home" view ---

# --- Sidebar: Time Range, Meeting selector, Economic Term Search ---
from sidebar import render_sidebar
from kpi import render_kpi_row
from kpi_details import render_kpi_detail
from utils import year_of
from backend.config import ALL_NGRAMS

@st.cache_data(ttl=60)
def fetch_meetings():
    resp = requests.get(f"{BACKEND_URL}/meetings")
    resp.raise_for_status()
    return resp.json()

@st.cache_data(ttl=60)
def fetch_overview():
    resp = requests.get(f"{BACKEND_URL}/sentiment/overview")
    resp.raise_for_status()
    return resp.json()

meetings = fetch_meetings()
meeting_dates = [m["date"] for m in meetings]

if not meeting_dates:
    st.error("No meetings found in the database. Run the ingest script first.")
    st.stop()



# --- Everything below only renders on the "home" view ---

ngram_options = sorted({" ".join(t) for n_list in ALL_NGRAMS.values() for t in n_list})

selected_year_range, selected_meeting, selected_term = render_sidebar(
    meeting_dates,
    ngram_options,
)

st.session_state["selected_year_range"] = selected_year_range
st.session_state["selected_meeting"] = selected_meeting
st.session_state["selected_term"] = selected_term

if current_view in ("kpi1", "kpi2", "kpi3"):
    render_kpi_detail(
        current_view,
        meetings,
        selected_year_range,
        ALL_NGRAMS,
    )
    st.stop()


# Make selections available to later steps (KPI cards, tabs) without re-threading params.
st.session_state["selected_year_range"] = selected_year_range
st.session_state["selected_meeting"] = selected_meeting
st.session_state["selected_term"] = selected_term

if selected_meeting is None:
    st.stop()  # sidebar already showed the "no meetings in range" warning

selected_date = selected_meeting  # keep existing variable name for the code below, unchanged

# --- KPI cards: computed from meetings/overview data filtered to the selected years ---
docs_in_range = [d for d in meeting_dates if selected_year_range[0] <= year_of(d) <= selected_year_range[1]]
documents_analyzed = len(docs_in_range)

concepts_tracked = sum(len(n_list) for n_list in ALL_NGRAMS.values())  # static, per config

overview = fetch_overview()
df_overview_kpi = pd.DataFrame(overview)
if not df_overview_kpi.empty:
    df_overview_kpi["year"] = df_overview_kpi["date"].apply(year_of)
    in_range = df_overview_kpi[
        (df_overview_kpi["year"] >= selected_year_range[0])
        & (df_overview_kpi["year"] <= selected_year_range[1])
    ]
    avg_sentiment = in_range["overall_sentiment"].mean() if not in_range.empty else 0.0
else:
    avg_sentiment = 0.0

render_kpi_row(documents_analyzed, concepts_tracked, avg_sentiment)

if selected_meeting is None:
    st.stop()  # sidebar already showed the "no meetings in range" warning

selected_date = selected_meeting  # keep existing variable name for the code below, unchanged

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
