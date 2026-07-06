import streamlit as st
 
 
def render_footer():
    footer_cols = st.columns(3)
    with footer_cols[0]:
        st.caption("LAST UPDATED")
        st.markdown("**2026-07-06**")
    with footer_cols[1]:
        st.link_button(
            "Methodology",
            "https://www.nber.org/system/files/working_papers/w32417/w32417.pdf",
            icon=":material/north_east:",
        )
    with footer_cols[2]:
        st.link_button(
            "Dictionary",
            "https://sraf.nd.edu/loughranmcdonald-master-dictionary/",
            icon=":material/north_east:",
        )
 