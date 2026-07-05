"""
Visual theme for the FOMC Sentiment Dashboard: 
font, color palette, andreusable CSS classes (cards, buttons, header).
"""

import streamlit as st

# --- Palette ---
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
    font-family: 'Source Serif Pro', serif;
}}

.stApp {{
    background-color: {COLOR_BG};
}}

/* Tighten default Streamlit top padding */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

/* Reusable card container for KPI cards, panels, etc. */
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