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
from frontend.faq import render_faq_page


BACKEND_URL = "https:/fed-policy-sentiment-api.onrender.com/"

st.set_page_config(page_title="FOMC Sentiment Dashboard", layout="wide")

inject_theme()
init_view_state()

def get_concepts_summary_if_needed(view, year_range):
    if view != "kpi2":
        return None
    return fetch_concepts_summary(year_range[0], year_range[1])

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
        if st.button("Home", key="home_nav_button", icon=":material/home:"):
            go_to("home")
    else:
        if st.button("FAQs", key="faq_nav_button", icon=":material/help:"):
            go_to("faq")

# --- FAQ page ---
if current_view == "faq":
    render_faq_page()
    st.stop()

# --- Everything below this only renders on the "home" view ---

# --- Sidebar: Time Range, Meeting selector, Economic Term Search ---
from sidebar import render_sidebar
from kpi import render_kpi_row
from kpi_details import render_kpi_detail
from utils import year_of
from tabs import render_meeting_overview_tab, render_time_series_tab, render_term_explorer_tab
from footer import render_footer
from backend.config import ALL_NGRAMS, INCLUDE_DICT

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

@st.cache_data(ttl=60)
def fetch_concepts_summary(start_year: int, end_year: int):
    resp = requests.get(
        f"{BACKEND_URL}/concepts/summary",
        params={"start_year": start_year, "end_year": end_year},
    )
    resp.raise_for_status()
    return resp.json()

@st.cache_data(ttl=60)
def fetch_meeting_sentiment(date):
    resp = requests.get(f"{BACKEND_URL}/meetings/{date}/sentiment")
    resp.raise_for_status()
    return resp.json()
 
 
@st.cache_data(ttl=60)
def fetch_ngram_trend(ngram: str):
    resp = requests.get(f"{BACKEND_URL}/sentiment/trend", params={"ngram": ngram.lower()})
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
    df["date"] = pd.to_datetime(df["date"], format="%Y_%m_%d")
    return df

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

    concepts_summary = get_concepts_summary_if_needed(
        current_view,
        selected_year_range
    )

    render_kpi_detail(
        current_view,
        meetings,
        selected_year_range,
        ALL_NGRAMS,
        concepts_summary
    )

    st.stop()


# Make selections available to later steps (KPI cards, tabs) without re-threading params.
st.session_state["selected_year_range"] = selected_year_range
st.session_state["selected_meeting"] = selected_meeting
st.session_state["selected_term"] = selected_term

if selected_meeting is None:
    st.stop()  # sidebar already showed the "no meetings in range" warning

selected_date = selected_meeting  # keep existing variable name for the code below, unchanged


# --- KPI detail views: full-page (reached via expand icons) ---
if current_view in ("kpi1", "kpi2", "kpi3"):
    concepts_summary = get_concepts_summary_if_needed(current_view, selected_year_range)
    render_kpi_detail(current_view, meetings, selected_year_range, ALL_NGRAMS, concepts_summary)
    st.stop()
 
# --- Everything below only renders on the "home" view ---
 
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
 
# So the KPI3 detail page can show the same number without recomputing it.
st.session_state["avg_sentiment_value"] = avg_sentiment
 
render_kpi_row(documents_analyzed, concepts_tracked, avg_sentiment)

st.markdown('<div class="kpi-row-spacer"></div>', unsafe_allow_html=True)

 
# Sync the sidebar's term search into the Term Explorer tab's active term,
# but only when the sidebar selection actually changes — so clicking a
# "related term" inside the tab isn't immediately overwritten on rerun.
if selected_term and selected_term != st.session_state.get("_last_sidebar_term"):
    st.session_state["term_explorer_active"] = selected_term
st.session_state["_last_sidebar_term"] = selected_term
 
df_overview_tabs = pd.DataFrame(overview)  # reuse the same fetch, no second network call
df_overview_tabs["date"] = pd.to_datetime(df_overview_tabs["date"], format="%Y_%m_%d")

with st.container(border=True, key="tabs_wrapper"):
    meeting_overview_tab, time_series_tab, term_explorer_tab = st.tabs(
        [
            ":material/visibility: Meeting Overview",
            ":material/show_chart: Time Series Trend",
            ":material/search: Term Explorer",
        ]
    )
    
    with meeting_overview_tab:
        st.caption(f"Selected meeting: {selected_date}")
        render_meeting_overview_tab(fetch_meeting_sentiment(selected_date))
    
    with time_series_tab:
        render_time_series_tab(df_overview_tabs, selected_year_range)
    
    with term_explorer_tab:
        render_term_explorer_tab(ngram_options, INCLUDE_DICT, fetch_ngram_trend)
    

st.markdown("---")
render_footer()