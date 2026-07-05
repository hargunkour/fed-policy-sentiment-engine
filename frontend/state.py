"""
Lightweight page-view router built on st.session_state. Lets buttons
(FAQs, Home, KPI expand icons, prev/next arrows) switch between logical
"pages" within the single Streamlit script, without Streamlit's native
multipage file-based routing (which doesn't support passing state like
"which KPI card triggered this" as cleanly).

Views used across this app: "home", "faq", "kpi1", "kpi2", "kpi3".
"""

import streamlit as st

DEFAULT_VIEW = "home"
_STATE_KEY = "view"


def init_view_state():
    """Call once per script run, before reading/using the current view."""
    if _STATE_KEY not in st.session_state:
        st.session_state[_STATE_KEY] = DEFAULT_VIEW


def get_view() -> str:
    return st.session_state.get(_STATE_KEY, DEFAULT_VIEW)


def go_to(view_name: str):
    """Switch views and immediately rerun so the new view renders this pass."""
    st.session_state[_STATE_KEY] = view_name
    st.rerun()