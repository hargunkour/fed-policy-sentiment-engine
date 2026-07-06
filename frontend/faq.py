"""
Renders the FAQ page. 
"""

import streamlit as st


def render_faq_page():

    st.markdown(
        '<h1 class="font-serif" style="text-align:center; margin-top:-0.5rem;">Frequently Asked Questions</h1>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    with st.expander("What is this project?"):
        st.markdown(
            "An NLP dashboard that scores FOMC meeting minutes for hawkish/dovish "
            "sentiment using the Loughran-McDonald financial dictionary. It tracks "
            "a fixed set of economic concepts (unigrams, bigrams, and trigrams) "
            "across every meeting from 1996 onward, and surfaces how the "
            "sentiment attached to those concepts shifts over time."
        )

    with st.expander("What is the FOMC?"):
        st.markdown(
            "The Federal Open Market Committee (FOMC) is the branch of the U.S. "
            "Federal Reserve responsible for setting monetary policy, including "
            "decisions on interest rates and the money supply, in pursuit of "
            "stable prices and maximum employment."
        )

    with st.expander("What do \"hawkish\" and \"dovish\" mean?"):
        col_hawk, col_dove = st.columns(2)
        with col_hawk:
            st.markdown("**Hawkish**")
            st.markdown(
                "Indicates a preference for tighter monetary policy, often through "
                "higher interest rates, to control inflation. Hawks are typically "
                "more concerned about inflation than economic growth."
            )
        with col_dove:
            st.markdown("**Dovish**")
            st.markdown(
                "Indicates a preference for supporting economic growth through "
                "lower interest rates or accommodative policy. Doves prioritize "
                "employment and economic expansion over low inflation."
            )

    with st.expander("What are n-grams?"):
        st.markdown(
            "An n-gram is a sequence of consecutive words. This project tracks "
            "three lengths:"
        )
        st.markdown(
            "- **Unigram** (1 word): `inflation`\n"
            "- **Bigram** (2 words): `interest rates`\n"
            "- **Trigram** (3 words): `consumer price index`"
        )
        st.markdown(
            "Tracking multi-word phrases, not just single words, captures "
            "economic concepts more precisely than single words alone."
        )

    with st.expander("How is sentiment measured?"):
        st.markdown(
            "Each tracked n-gram is scored using the Loughran-McDonald financial "
            "sentiment dictionary. Rather than scoring the term in isolation, the "
            "words immediately surrounding each occurrence are also scored, so "
            "the same term can register differently depending on its context "
            "within the document. Scores are then aggregated per meeting and "
            "normalized by document length."
        )

    with st.expander("What inspired this project?"):
        st.markdown(
            "This project's methodology is inspired by *Identifying Monetary "
            "Policy Shocks: A Natural Language Approach* by S. Borağan Aruoba "
            "and Thomas Drechsel. While the sentiment-scoring approach draws on "
            "their research, this dashboard is an **independent implementation** "
            "built from scratch — including the data pipeline, database, API, "
            "and visualizations — and is not affiliated with the original "
            "authors or their published results."
        )

    st.markdown("---")

    footer_cols = st.columns(3)
    with footer_cols[0]:
        st.caption("LAST UPDATED")
        st.markdown("**2026-05-14**")
    with footer_cols[1]:
        st.caption("METHODOLOGY")
    with footer_cols[2]:
        st.caption("DICTIONARY")
