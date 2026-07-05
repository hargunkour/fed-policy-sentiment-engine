"""
Visual theme for the FOMC Sentiment Dashboard: font, color palette, and
reusable CSS classes (cards, buttons, header). Injected once per page
load via inject_theme(). Pure styling — no data or routing logic, and
no CSS used to position widgets (button placement is handled entirely
by Streamlit layout primitives in kpi.py / kpi_details.py).
"""

import streamlit as st

# --- Palette (from Figma) ---
COLOR_ACCENT = "#506FC8"
COLOR_BG = "#D9D9D9"
COLOR_CARD = "#FFFFFF"
COLOR_BORDER = "#E0E0E0"
COLOR_POSITIVE = "#2E7D32"
COLOR_NEGATIVE = "#C62828"
COLOR_TEXT = "#1A1A2E"

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'IBM Plex Sans', sans-serif;
}}

.stApp {{
    background-color: {COLOR_BG};
}}

/* Tighten default Streamlit top padding so the header sits like a real dashboard */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

/* Reusable card container for panels (FAQ placeholder, etc.) */
.dashboard-card {{
    background-color: {COLOR_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}}

.dashboard-title {{
    color: {COLOR_ACCENT};
    font-weight: 700;
    margin-bottom: 0;
}}

.dashboard-subtitle {{
    color: {COLOR_TEXT};
    opacity: 0.75;
    font-weight: 500;
    margin-top: -0.5rem;
}}

.kpi-value-positive {{ color: {COLOR_POSITIVE}; font-weight: 700; }}
.kpi-value-negative {{ color: {COLOR_NEGATIVE}; font-weight: 700; }}

/* KPI detail page: centered white info card. Static box styling only —
   its position on the page comes from margin: auto, not from any
   widget-positioning CSS. */
.kpi-detail-inner-card {{
    background-color: {COLOR_CARD};
    border-radius: 12px;
    padding: 2rem 2.5rem;
    max-width: 520px;
    margin: 1rem auto;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}}

.kpi-detail-row {{
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0;
    font-size: 1rem;
    color: #4A5568;
}}

.arrow-column{{
    display:flex;
    justify-content:center;
    align-items:center;
    height:340px;
}}

/* Ghost/link-style button used for FAQs and Home nav */
div[data-testid="stButton"] > button.ghost-nav {{
    background: transparent;
    border: none;
    color: {COLOR_ACCENT};
    font-weight: 600;
}}
</style>
"""


def inject_theme():
    """Injects the dashboard's global CSS. Call once near the top of app.py."""
    st.markdown(_CSS, unsafe_allow_html=True)