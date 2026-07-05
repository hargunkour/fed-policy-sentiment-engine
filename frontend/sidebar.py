"""
Renders the dashboard's sidebar: Time Range slider, Meeting selector
(scoped to the selected years), and Economic Term Search. Pure
presentation — takes data in, returns the user's selections. Callers
are responsible for fetching data and for acting on the returned values.
"""

import streamlit as st


def _year_of(date_str: str) -> int:
    """Meeting dates are stored as 'YYYY_MM_DD'."""
    return int(date_str.split("_")[0])


def render_sidebar(meeting_dates: list[str], ngram_options: list[str]):
    """
    meeting_dates: full list of meeting date strings from /meetings (unfiltered).
    ngram_options: full list of trackable n-gram strings for the search box.

    Returns: (year_range, selected_meeting, selected_term)
        year_range: (start_year, end_year) tuple, inclusive
        selected_meeting: date string, or None if no meetings fall in range
        selected_term: string, or "" if nothing selected
    """
    with st.sidebar:
        st.markdown("### Time Range")
        years = sorted({_year_of(d) for d in meeting_dates})
        min_year, max_year = years[0], years[-1]
        year_range = st.slider(
            "Select year range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            label_visibility="collapsed",
        )

        st.markdown("### Select Meeting")
        filtered_dates = [
            d for d in meeting_dates
            if year_range[0] <= _year_of(d) <= year_range[1]
        ]
        if not filtered_dates:
            st.warning("No meetings in the selected year range.")
            selected_meeting = None
        else:
            selected_meeting = st.selectbox(
                "Meeting date",
                filtered_dates,
                label_visibility="collapsed",
            )

        st.markdown("### Economic Term Search")
        selected_term = st.selectbox(
            "Search terms",
            options=[""] + ngram_options,
            format_func=lambda t: "Start typing..." if t == "" else t,
            label_visibility="collapsed",
        )

    return year_range, selected_meeting, selected_term