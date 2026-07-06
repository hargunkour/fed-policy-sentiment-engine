"""
Visual theme for the FOMC Sentiment Dashboard — "financial editorial"
style: Source Serif 4 for headings/big numbers, Public Sans for body
and labels, a warm cream/near-black/green/red palette (from Figma).

Injected once per page load via inject_theme(). Pure styling — no data
or routing logic, and no CSS used to position widgets.
"""

import streamlit as st
 
# --- Palette (from Figma "Selection colors") ---
COLOR_BG = "#F5F4EB"           # page background (warm cream)
COLOR_CARD = "#FFFFFF"         # card background
COLOR_CARD_ALT = "#FBF9F1"     # slightly warmer card variant (insights box, etc.)
COLOR_TEXT = "#1B1C17"         # near-black, primary text
COLOR_MUTED = "#444748"        # secondary text, small labels
COLOR_BORDER = "#C4C7C7"       # hairline borders/dividers
COLOR_POSITIVE = "#005232"     # dovish / positive — deep green
COLOR_NEGATIVE = "#93000A"     # hawkish / negative — deep red
COLOR_NEGATIVE_STRONG = "#BA1A1A"   # hover/emphasis red
COLOR_NEGATIVE_CONTAINER = "#FFDAD6"  # light pink tint (negative chips/backgrounds)
COLOR_NEUTRAL_CONTAINER = "#F0EEE5"   # light neutral tint (pills, subtle fills)
 
_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Public+Sans:wght@400;500;600;700&display=swap');
 
html, body, [class*="css"] {{
    font-family: 'Public Sans', sans-serif;
    color: {COLOR_TEXT};
}}
 
h1, h2, h3, .font-serif {{
    font-family: 'Source Serif 4', serif;
}}
 
.stApp {{
    background-color: {COLOR_BG};
}}
 
.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}
 
/* --- Cards: thin hairline border, minimal shadow, slight rounding --- */
.dashboard-card {{
    background-color: {COLOR_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
}}
 
.dashboard-title {{
    font-family: 'Source Serif 4', serif;
    color: {COLOR_TEXT};
    font-weight: 700;
    margin-bottom: 0;
}}
 
.dashboard-subtitle {{
    font-family: 'Public Sans', sans-serif;
    color: {COLOR_MUTED};
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-size: 0.8rem;
    margin-top: 0.1rem;
}}
 
/* Small uppercase section labels ("SENTIMENT INSIGHTS", "RELATED SEMANTIC
   NODES", KPI card titles, etc.) — the recurring editorial-caption style */
.section-label {{
    font-family: 'Public Sans', sans-serif;
    color: {COLOR_MUTED};
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-size: 0.75rem;
}}
 
.kpi-value-positive {{ color: {COLOR_POSITIVE}; font-weight: 700; }}
.kpi-value-negative {{ color: {COLOR_NEGATIVE}; font-weight: 700; }}
 
/* --- KPI detail page: centered white info card --- */
.kpi-detail-inner-card {{
    background-color: {COLOR_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 10px;
    padding: 2rem 2.5rem;
    max-width: 520px;
    margin: 1rem auto;
}}
 
.kpi-detail-row {{
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    font-size: 1rem;
    color: {COLOR_TEXT};
    border-bottom: 1px solid {COLOR_NEUTRAL_CONTAINER};
}}
.kpi-detail-row:last-child {{ border-bottom: none; }}
 
/* --- Circular icon buttons: KPI-detail Back/Next arrows ---
   The button is a SIBLING of the marker span (Streamlit wraps every
   st.markdown/st.button call in its own container, so a widget can't
   truly be nested inside a div). We render a tiny marker span right
   before the button, then use :has() to find "the stButton block that
   immediately follows a marker" and style THAT button — this is a
   real sibling relationship, unlike wrapping, so it reliably matches. */
div[data-testid="stMarkdown"]:has(.arrow-marker) + div[data-testid="stButton"] button {{
    border-radius: 50% !important;
    width: 2.75rem !important;
    height: 2.75rem !important;
    padding: 0 !important;
    background-color: {COLOR_NEUTRAL_CONTAINER} !important;
    border: 1px solid {COLOR_BORDER} !important;
    color: {COLOR_TEXT} !important;
    font-size: 1.1rem !important;
}}
div[data-testid="stMarkdown"]:has(.arrow-marker) + div[data-testid="stButton"] button:hover {{
    background-color: {COLOR_BORDER} !important;
}}
 
/* --- Pill buttons: related-terms / semantic-node chips (same marker technique) --- */
div[data-testid="stMarkdown"]:has(.pill-marker) + div[data-testid="stButton"] button {{
    background-color: {COLOR_CARD} !important;
    border: 1px solid {COLOR_BORDER} !important;
    border-radius: 999px !important;
    color: {COLOR_TEXT} !important;
    font-family: 'Public Sans', sans-serif;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.3rem 1rem !important;
    box-shadow: none !important;
}}
div[data-testid="stMarkdown"]:has(.pill-marker) + div[data-testid="stButton"] button:hover {{
    background-color: {COLOR_NEUTRAL_CONTAINER} !important;
    border-color: {COLOR_MUTED} !important;
}}
 
/* --- Streamlit tabs: underline style, no default blue --- */
.stTabs [data-baseweb="tab-list"] {{
    gap: 1.5rem;
    border-bottom: 1px solid {COLOR_BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'Public Sans', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    color: {COLOR_MUTED};
    letter-spacing: 0.03em;
    text-transform: uppercase;
    padding-bottom: 0.6rem;
}}
.stTabs [aria-selected="true"] {{
    color: {COLOR_TEXT} !important;
    border-bottom: 2px solid {COLOR_TEXT} !important;
}}
 
/* Inline highlighted phrases inside Sentiment Insights */
.insight-positive {{ color: {COLOR_POSITIVE}; font-weight: 600; }}
.insight-negative {{ color: {COLOR_NEGATIVE}; font-weight: 600; }}
.insight-quote {{ font-style: italic; color: {COLOR_MUTED}; }}
</style>
"""
 
 
def inject_theme():
    """Injects the dashboard's global CSS. Call once near the top of app.py."""
    st.markdown(_CSS, unsafe_allow_html=True)